# Neuer Ansatz für Terraform AWS-Kostenanalyse mit Filtersystem
import boto3
import json
import argparse
from datetime import datetime
from tabulate import tabulate

from filter import ec2_filters, ebs_filters, nodegroup_meta, cluster_meta, eks_pricing_meta, pricing_defaults, duration_meta

TF_PLAN_FILE = "../terraform-faregate.plan.json"
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
        print(f"⚠️  Keine Release-Info gefunden, Standardrate wird verwendet.")
        return pricing_defaults.CONTROL_PLANE_STANDARD_RATE * hours

    current_date = datetime.now()
    months_since_release = (current_date.year - release_date.year) * 12 + current_date.month - release_date.month

    if months_since_release <= 14:
        return pricing_defaults.CONTROL_PLANE_STANDARD_RATE * hours
    elif months_since_release <= 26:
        return pricing_defaults.CONTROL_PLANE_EXTENDED_RATE * hours
    else:
        print(f"⚠️  Kubernetes-Version wird möglicherweise nicht mehr unterstützt.")
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


def get_ec2_price(pricing_client, filters):
    try:
        response = pricing_client.get_products(
            ServiceCode="AmazonEC2",
            Filters=filters,
            MaxResults=1
        )
        for item in response.get("PriceList", []):
            offer = json.loads(item)
            terms = offer.get("terms", {}).get("OnDemand", {})
            for term in terms.values():
                dimensions = term.get("priceDimensions", {})
                for dim in dimensions.values():
                    price = dim.get("pricePerUnit", {}).get("USD")
                    if price:
                        print(f"🔍 Gefundener EC2 Preis: {price} USD für Filter: {json.dumps(filters, indent=2)}")
                        return float(price)
    except Exception as e:
        print(f"⚠️ Fehler bei EC2-Preisabfrage: {e}")
    return 0.0


def get_spot_price(ec2_client, instance_type, availability_zone="eu-central-1a"):
    try:
        prices = ec2_client.describe_spot_price_history(
            InstanceTypes=[instance_type],
            ProductDescriptions=["Linux/UNIX"],
            AvailabilityZone=availability_zone,
            MaxResults=1
        )
        if prices["SpotPriceHistory"]:
            price = float(prices["SpotPriceHistory"][0]["SpotPrice"])
            print(f"☁️  Spotpreis {instance_type} in {availability_zone}: ${price:.4f} USD")
            return price
    except Exception as e:
        print(f"⚠️ Fehler bei Spot-Preisabfrage: {e}")
    return 0.0


def main():
    args = parse_args()
    with open(args.plan) as f:
        plan = json.load(f)

    pricing = boto3.client("pricing", region_name="us-east-1")
    ec2_client = boto3.client("ec2")
    use_fargate = detect_fargate_usage(plan)

    relevant_resources = extract_relevant_resources(args.plan)
    print("✅ Verarbeitete Terraform-Ressourcentypen:")
    for r in relevant_resources:
        print(" -", r)

    instance_type, capacity_type, desired_size = nodegroup_meta.extract(plan)
    region = "EU (Frankfurt)"
    marketoption = "OnDemand" if capacity_type.upper() == "ON_DEMAND" else "Spot"

    ec2 = ec2_filters.build(instance_type, region, marketoption)
    ebs = ebs_filters.build("gp3", region)

    print("\n📦 EC2 Filter:")
    print(json.dumps(ec2, indent=2))

    print("\n💾 EBS Filter:")
    print(json.dumps(ebs, indent=2))

    print(f"\n👥 Desired Node Count: {desired_size}")

    table = []
    total_cost = 0.0

    # Kontrollplane-Kosten berechnen
    k8s_version = cluster_meta.extract_version(plan)
    if k8s_version:
        release_date = eks_pricing_meta.get_release_date(k8s_version)
        cp_cost = round(calculate_control_plane_cost(release_date, hours=HOURS_PER_MONTH), 5)
        total_cost += cp_cost
        table.append(["Control Plane", 1, f"v{k8s_version}", f"${cp_cost:.5f}"])
    else:
        print("⚠️  Keine Kubernetes-Version im Plan gefunden – Kontrollplane-Kosten nicht berechnet.")

    # Node Group (EC2) nur wenn kein Fargate genutzt wird
    if instance_type and desired_size > 0 and not use_fargate:
        if marketoption == "OnDemand":
            ec2_unit_cost = get_ec2_price(pricing, ec2)
        else:
            ec2_unit_cost = get_spot_price(ec2_client, instance_type)
        ec2_cost = round(ec2_unit_cost * desired_size * HOURS_PER_MONTH, 5)
        table.append(["Node Group (EC2)", desired_size, instance_type, f"${ec2_cost:.5f}"])
        total_cost += ec2_cost

    # EBS Volumes nur wenn keine Fargate-Nutzung
    if desired_size > 0 and not use_fargate:
        ebs_price_per_gb = pricing_defaults.AMAZON_EBS
        ebs_cost = round((ebs_price_per_gb * 20 / 730) * desired_size * HOURS_PER_MONTH, 5)
        table.append(["EBS Volumes", desired_size, "gp3 (20 GB)", f"${ebs_cost:.5f}"])
        total_cost += ebs_cost

    # Fargate
    if use_fargate:
        fargate_cost = calculate_fargate_cost(hours=HOURS_PER_MONTH)
        table.append([
            "Fargate",
            pricing_defaults.FARGATE_DEFAULT_PODS,
            f"{pricing_defaults.FARGATE_DEFAULT_VCPU}vCPU/{pricing_defaults.FARGATE_DEFAULT_RAM_GB}GB",
            f"${fargate_cost:.5f}"
        ])
        total_cost += fargate_cost

    print("\n📊 EKS Kostenübersicht (pro Monat)")
    print(tabulate(table, headers=["Komponente", "Anzahl", "Typ", "Kosten"], tablefmt="github"))
    print(f"\n💰 Gesamtkosten/Monat: ${round(total_cost, 5)}")


if __name__ == "__main__":
    main()
