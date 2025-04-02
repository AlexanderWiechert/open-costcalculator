# main.py
import boto3
import json
import argparse
from datetime import datetime
from tabulate import tabulate
import sys
from pathlib import Path

from filter import ec2_filters, ebs_filters, nodegroup_meta, cluster_meta, eks_pricing_meta, pricing_defaults, duration_meta, nat_gateway_filter, nat_gateway_meta, rds_filters, rds_meta, rds_utils, pricing_utils

TF_PLAN_FILE = "../test/terraform.plan.json"
IGNORED_PREFIXES = ["aws_iam_", "aws_network_acl", "aws_vpc", "aws_subnet", "aws_route", "aws_default_", "aws_internet_gateway"]
IGNORED_RESOURCE_TYPES = ["null_resource", "local_file", "random_", "external"]

HOURS_PER_MONTH = duration_meta.HOURS_PER_MONTH  # zentral gepflegt

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", default=TF_PLAN_FILE, help="Pfad zur terraform.plan.json Datei")
    return parser.parse_args()

def is_relevant_resource(resource_type):
    return not any(resource_type.startswith(prefix) for prefix in IGNORED_PREFIXES + IGNORED_RESOURCE_TYPES)

def extract_relevant_resources(plan_path):
    with open(plan_path) as f:
        plan = json.load(f)

    relevant = []
    for change in plan.get("resource_changes", []):
        rtype = change.get("type")
        if is_relevant_resource(rtype):
            relevant.append(rtype)
    return sorted(set(relevant))

def calculate_control_plane_cost(release_date, hours):
    if not release_date:
        return pricing_defaults.CONTROL_PLANE_STANDARD_RATE * hours

    current_date = datetime.now()
    months_since_release = (current_date.year - release_date.year) * 12 + current_date.month - release_date.month

    if months_since_release <= 14:
        return pricing_defaults.CONTROL_PLANE_STANDARD_RATE * hours
    elif months_since_release <= 26:
        return pricing_defaults.CONTROL_PLANE_EXTENDED_RATE * hours
    else:
        return 0.0

def detect_fargate_usage(plan):
    for res in plan.get("resource_changes", []):
        if res.get("type") == "aws_eks_fargate_profile":
            return True
    return False

def calculate_fargate_cost(hours):
    cpu_cost = pricing_defaults.FARGATE_VCPU_RATE * pricing_defaults.FARGATE_DEFAULT_VCPU
    ram_cost = pricing_defaults.FARGATE_RAM_RATE * pricing_defaults.FARGATE_DEFAULT_RAM_GB
    total_per_pod = (cpu_cost + ram_cost) * hours
    return round(total_per_pod * pricing_defaults.FARGATE_DEFAULT_PODS, 5)

def detect_alb_from_controller(plan):
    for res in plan.get("resource_changes", []):
        if res.get("type") == "helm_release":
            chart = res.get("change", {}).get("after", {}).get("chart", "")
            if "aws-load-balancer-controller" in chart:
                return True
    return False

def detect_alb_resources(plan):
    for res in plan.get("resource_changes", []):
        if res.get("type") == "aws_lb" and res.get("change", {}).get("after", {}).get("load_balancer_type") == "application":
            return True
    return False

def count_albs(plan):
    return sum(
        1 for res in plan.get("resource_changes", [])
        if res.get("type") == "aws_lb" and res.get("change", {}).get("after", {}).get("load_balancer_type") == "application"
    )

def extract_rds_info(plan):
    modules = [plan["planned_values"]["root_module"]]
    while modules:
        module = modules.pop()
        for res in module.get("resources", []):
            if res.get("type") == "aws_db_instance":
                values = res.get("values", {})
                return {
                    "instance_class": values.get("instance_class"),
                    "engine": values.get("engine"),
                    "storage_type": values.get("storage_type"),
                    "storage_gb": values.get("allocated_storage"),
                    "multi_az": values.get("multi_az", False)
                }
        modules.extend(module.get("child_modules", []))
    return None

def main():
    args = parse_args()

    plan_path = Path(args.plan)
    if not plan_path.is_file():
        print(f"❌ Fehler: Die angegebene Datei '{args.plan}' wurde nicht gefunden.")
        sys.exit(1)

    with open(args.plan) as f:
        plan = json.load(f)

    pricing = boto3.client("pricing", region_name="us-east-1")
    ec2_client = boto3.client("ec2")
    use_fargate = detect_fargate_usage(plan)

    instance_type, capacity_type, desired_size = nodegroup_meta.extract(plan)
    region = "EU (Frankfurt)"

    if capacity_type:
        marketoption = "OnDemand" if capacity_type.upper() == "ON_DEMAND" else "Spot"
    else:
        print("⚠️  Keine capacity_type gefunden – fallback zu 'OnDemand'")
        marketoption = "OnDemand"

    ec2 = ec2_filters.build(instance_type, region, marketoption)
    ebs = ebs_filters.build("gp3", region)

    table = []
    total_cost = 0.0

    k8s_version = cluster_meta.extract_version(plan)
    if k8s_version:
        release_date = eks_pricing_meta.get_release_date(k8s_version)
        cp_cost = round(calculate_control_plane_cost(release_date, hours=HOURS_PER_MONTH), 5)
        total_cost += cp_cost
        table.append(["Control Plane", 1, f"v{k8s_version}", f"${cp_cost:.5f}"])

    if instance_type and desired_size > 0 and not use_fargate:
        if marketoption == "OnDemand":
            ec2_unit_cost = pricing_utils.get_price(pricing, "AmazonEC2", ec2)
        else:
            ec2_unit_cost = pricing_utils.get_spot_price(ec2_client, instance_type)
        ec2_cost = round(ec2_unit_cost * desired_size * HOURS_PER_MONTH, 5)
        table.append(["Node Group (EC2)", desired_size, instance_type, f"${ec2_cost:.5f}"])
        total_cost += ec2_cost

    if desired_size > 0 and not use_fargate:
        ebs_price_per_gb = pricing_defaults.EBS_STORAGE_PRICING.get("gp3", 0.08)
        ebs_cost = round((ebs_price_per_gb * 20 / 730) * desired_size * HOURS_PER_MONTH, 5)
        table.append(["EBS Volumes", desired_size, "gp3 (20 GB)", f"${ebs_cost:.5f}"])
        total_cost += ebs_cost

    if use_fargate:
        fargate_cost = calculate_fargate_cost(hours=HOURS_PER_MONTH)
        table.append([
            "Fargate",
            pricing_defaults.FARGATE_DEFAULT_PODS,
            f"{pricing_defaults.FARGATE_DEFAULT_VCPU}vCPU/{pricing_defaults.FARGATE_DEFAULT_RAM_GB}GB",
            f"${fargate_cost:.5f}"
        ])
        total_cost += fargate_cost

    alb_count = count_albs(plan)
    if detect_alb_from_controller(plan) or alb_count > 0:
        alb_cost = round((pricing_defaults.ALB_HOURLY_RATE + pricing_defaults.ALB_LCU_RATE * pricing_defaults.ALB_ASSUMED_LCU) * HOURS_PER_MONTH, 5) * max(alb_count, 1)
        table.append(["ALB (geschätzt)", alb_count or 1, f"{pricing_defaults.ALB_ASSUMED_LCU} LCU", f"${alb_cost:.5f}"])
        total_cost += alb_cost

    nat_count = nat_gateway_meta.count(plan)
    if nat_count > 0:
        nat_filters = nat_gateway_filter.build(region)
        nat_unit_price = pricing_utils.get_price(pricing, "AmazonVPC", nat_filters)
        nat_cost = round(nat_unit_price * nat_count * HOURS_PER_MONTH, 5)
        table.append(["NAT Gateway", nat_count, "Standard", f"${nat_cost:.5f}"])
        total_cost += nat_cost

    rds_info = extract_rds_info(plan)
    if rds_info:
        rds_filter = rds_filters.build(
            rds_info["instance_class"],
            rds_info["engine"],
            region,
            rds_info["multi_az"]
        )
        rds_instance_price = pricing_utils.get_price(pricing, "AmazonRDS", rds_filter)
        rds_storage_price_per_gb = rds_utils.get_rds_storage_price(pricing, rds_info["storage_type"], region)
        rds_instance_cost = round(rds_instance_price * HOURS_PER_MONTH, 5)
        rds_storage_cost = round(rds_storage_price_per_gb * rds_info["storage_gb"], 5)
        table.append(["RDS Instance", 1, rds_info["instance_class"], f"${rds_instance_cost:.5f}"])
        table.append(["RDS Storage", rds_info["storage_gb"], f"{rds_info['storage_type']}", f"${rds_storage_cost:.5f}"])
        total_cost += rds_instance_cost + rds_storage_cost

    print("\n📊 EKS Kostenübersicht (pro Monat)")
    print(tabulate(table, headers=["Komponente", "Anzahl", "Typ", "Kosten"], tablefmt="github"))
    print(f"\n💰 Gesamtkosten/Monat: ${round(total_cost, 5)}")

if __name__ == "__main__":
    main()
