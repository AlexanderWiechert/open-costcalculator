# main.py
import boto3
import json
import argparse
from datetime import datetime
from tabulate import tabulate
import sys
from pathlib import Path

from filter import *
from filter import logger, rds_costs, fargate_costs

TF_PLAN_FILE = "../test/terraform-sf2l.plan.json"
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

def extract_region_from_plan(plan):
    try:
        root = plan["configuration"]["provider_config"]["aws"]["expressions"]
        if "region" in root:
            return root["region"]["constant"]
    except Exception:
        pass
    return "EU (Frankfurt)"  # Fallback

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

def detect_resource(plan, resource_type, condition=None):
    return any(
        res.get("type") == resource_type and (condition(res) if condition else True)
        for res in plan.get("resource_changes", [])
    )

def count_resources(plan, resource_type, condition=None):
    return sum(
        1 for res in plan.get("resource_changes", [])
        if res.get("type") == resource_type and (condition(res) if condition else True)
    )

def detect_fargate_usage(plan):
    return detect_resource(plan, "aws_eks_fargate_profile")

def detect_alb_from_controller(plan):
    return detect_resource(plan, "helm_release", lambda r: "aws-load-balancer-controller" in r.get("change", {}).get("after", {}).get("chart", ""))

def count_albs(plan):
    return count_resources(plan, "aws_lb", lambda r: r.get("change", {}).get("after", {}).get("load_balancer_type") == "application")

def print_summary_table(table, total_cost):
    logger.info("📊 EKS Kostenübersicht (pro Monat)")
    print(tabulate(table, headers=["Komponente", "Anzahl", "Typ", "Kosten"], tablefmt="github"))
    logger.info(f"💰 Gesamtkosten/Monat: ${round(total_cost, 5)}")

def process_node_group(pricing, ec2_client, instance_type, desired_size, marketoption, region):
    ec2 = ec2_filters.build(instance_type, region, marketoption)
    ec2_unit_cost = pricing_utils.get_price(pricing, "AmazonEC2", ec2) if marketoption == "OnDemand" else pricing_utils.get_spot_price(ec2_client, instance_type)
    ec2_cost = round(ec2_unit_cost * desired_size * HOURS_PER_MONTH, 5)

    ebs_price_per_gb = pricing_defaults.EBS_STORAGE_PRICING.get("gp3", 0.08)
    ebs_cost = round((ebs_price_per_gb * 20 / 730) * desired_size * HOURS_PER_MONTH, 5)

    return [
        ["Node Group (EC2)", desired_size, instance_type, f"${ec2_cost:.5f}"],
        ["EBS Volumes", desired_size, "gp3 (20 GB)", f"${ebs_cost:.5f}"]
    ], ec2_cost + ebs_cost

def process_control_plane(plan, hours):
    k8s_version = cluster_meta.extract_version(plan)
    if not k8s_version:
        return [], 0.0
    release_date = eks_pricing_meta.get_release_date(k8s_version)
    cp_cost = round(calculate_control_plane_cost(release_date, hours=hours), 5)
    return [["Control Plane", 1, f"v{k8s_version}", f"${cp_cost:.5f}"]], cp_cost

def process_alb(plan, hours):
    alb_count = count_albs(plan)
    if detect_alb_from_controller(plan) or alb_count > 0:
        alb_cost = round((pricing_defaults.ALB_HOURLY_RATE + pricing_defaults.ALB_LCU_RATE * pricing_defaults.ALB_ASSUMED_LCU) * hours, 5) * max(alb_count, 1)
        return [["ALB (geschätzt)", alb_count or 1, f"{pricing_defaults.ALB_ASSUMED_LCU} LCU", f"${alb_cost:.5f}"]], alb_cost
    return [], 0.0

def process_nat_gateway(plan, pricing, region, hours):
    nat_count = nat_gateway_meta.count(plan)
    if nat_count > 0:
        nat_filters = nat_gateway_filter.build(region)
        nat_unit_price = pricing_utils.get_price(pricing, "AmazonVPC", nat_filters)
        nat_cost = round(nat_unit_price * nat_count * hours, 5)
        return [["NAT Gateway", nat_count, "Standard", f"${nat_cost:.5f}"]], nat_cost
    return [], 0.0

def process_fargate(hours):
    fargate_cost = fargate_costs.calculate_fargate_cost(hours)
    return [[
        "Fargate",
        pricing_defaults.FARGATE_DEFAULT_PODS,
        f"{pricing_defaults.FARGATE_DEFAULT_VCPU}vCPU/{pricing_defaults.FARGATE_DEFAULT_RAM_GB}GB",
        f"${fargate_cost:.5f}"
    ]], fargate_cost

def main():
    args = parse_args()
    plan_path = Path(args.plan)
    if not plan_path.is_file():
        logger.error(f"Die angegebene Datei '{args.plan}' wurde nicht gefunden.")
        sys.exit(1)

    with open(args.plan) as f:
        plan = json.load(f)

    region = extract_region_from_plan(plan)
    pricing = boto3.client("pricing", region_name="us-east-1")
    ec2_client = boto3.client("ec2")
    use_fargate = detect_fargate_usage(plan)

    instance_type, capacity_type, desired_size = nodegroup_meta.extract(plan)
    marketoption = "OnDemand" if not capacity_type or capacity_type.upper() == "ON_DEMAND" else "Spot"
    if not capacity_type:
        logger.warn("Keine capacity_type gefunden – fallback zu 'OnDemand'")

    table = []
    total_cost = 0.0

    rows, cost = process_control_plane(plan, HOURS_PER_MONTH)
    table.extend(rows)
    total_cost += cost

    if instance_type and desired_size > 0 and not use_fargate:
        rows, cost = process_node_group(pricing, ec2_client, instance_type, desired_size, marketoption, region)
        table.extend(rows)
        total_cost += cost

    if use_fargate:
        rows, cost = process_fargate(HOURS_PER_MONTH)
        table.extend(rows)
        total_cost += cost

    rows, cost = process_alb(plan, HOURS_PER_MONTH)
    table.extend(rows)
    total_cost += cost

    rows, cost = process_nat_gateway(plan, pricing, region, HOURS_PER_MONTH)
    table.extend(rows)
    total_cost += cost

    rds_rows, rds_total = rds_costs.calculate_rds_cost(pricing, plan, region, HOURS_PER_MONTH)
    table.extend(rds_rows)
    total_cost += rds_total

    print_summary_table(table, total_cost)

if __name__ == "__main__":
    main()
