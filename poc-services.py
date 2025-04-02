# Neuer Ansatz für Terraform AWS-Kostenanalyse
import boto3
import json
import argparse

TF_PLAN_FILE = "terraform.plan.json"
IGNORED_PREFIXES = ["aws_iam_", "aws_network_acl", "aws_vpc", "aws_subnet", "aws_route", "aws_default_", "aws_internet_gateway"]
IGNORED_RESOURCE_TYPES = ["null_resource", "local_file", "random_", "external"]

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


def main():
    args = parse_args()
    relevant_resources = extract_relevant_resources(args.plan)
    print("✅ Verarbeitete Terraform-Ressourcentypen:")
    for r in relevant_resources:
        print(" -", r)


if __name__ == "__main__":
    main()
