import argparse
import datetime
import json
from terraform_parser import load_tf_plan, extract_variables, extract_cost_info, extract_lambda_info, extract_apigw_info
from pricing.ec2_pricing import get_ec2_on_demand_price, get_ec2_spot_price, get_ec2_price_from_config
from pricing.lambda_pricing import query_lambda_price, extract_price_from_lambda_response
from pricing.apigw_pricing import query_apigw_price, extract_price_from_apigw_response
from config import load_config

def main():
    parser = argparse.ArgumentParser(description="Cost Query Script")
    parser.add_argument("--plan", action="store_true", help="Use Terraform plan (plan.json) for variable extraction")
    args = parser.parse_args()

    current_timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    if args.plan:
        plan = load_tf_plan("plans/plan.json")
        variables = extract_variables(plan)
        eks_info = extract_cost_info(plan)
        lambda_info = extract_lambda_info(plan)
        apigw_info = extract_apigw_info(plan)
    else:
        # Im Config-Modus: Lese Konfiguration aus config.yml und führe die EC2-Preisabfrage durch.
        config = load_config("config.yml")
        variables = config.get("pricing", {})
        ec2_output = get_ec2_price_from_config()
        # In diesem Zweig sind weitere Ressourcen (EKS, Lambda, API GW) nicht extrahiert.
        eks_info = []
        lambda_info = []
        apigw_info = []

    print("Extracted Variables:")
    print(json.dumps(variables, indent=2))

    if args.plan and eks_info:
        print("\nEKS Node Group Summary:")
        for info in eks_info:
            print(f"\nResource (eks_node_group): {info['resource']}")
            print(f"  Cluster Name: {info['cluster_name']}")
            print(f"  Capacity Type: {info['capacity_type']}")
            if info.get("desired_size") is not None:
                print(f"  Number of Instances: {info['desired_size']}")
            else:
                print("  Number of Instances: not defined")
            for instance_type in info["instance_types"]:
                if info["capacity_type"].upper() == "SPOT":
                    price = query_spot_price(instance_type, variables.get("region", "us-east-1"))
                else:
                    marketoption = "OnDemand"
                    response = query_on_demand_price(instance_type, variables.get("region", "us-east-1"), marketoption)
                    price = extract_price_from_on_demand_response(response)
                try:
                    price_float = float(price)
                except (TypeError, ValueError):
                    price_float = 0.0
                hourly_cost = price_float * (info.get("desired_size") or 1)
                print(f"  Instance Type: {instance_type}")
                print(f"  Hourly Cost: {hourly_cost} USD/h")
                print(f"  Timestamp: {current_timestamp}")

    if not args.plan:
        print("\nEC2 Price Output (from config):")
        print(json.dumps(ec2_output, indent=2))

    if lambda_info:
        print("\nLambda Function Summary:")
        for lam in lambda_info:
            print(f"\nResource (lambda): {lam['resource']}")
            print(f"  Function Name: {lam['function_name']}")
            print(f"  Runtime: {lam['runtime']}")
            print(f"  Memory Size: {lam['memory_size']} MB")
            response = query_lambda_price(lam["runtime"], lam["memory_size"])
            price = extract_price_from_lambda_response(response)
            try:
                price_float = float(price)
            except (TypeError, ValueError):
                price_float = 0.0
            print(f"  Price per duration unit: {price_float} USD")
            print(f"  Timestamp: {current_timestamp}")

    if apigw_info:
        print("\nAPI Gateway Summary:")
        for api in apigw_info:
            print(f"\nResource (apigw): {api['resource']}")
            print(f"  Name: {api['name']}")
            print(f"  Description: {api['description']}")
            response = query_apigw_price("REST")
            price = extract_price_from_apigw_response(response)
            try:
                price_float = float(price)
            except (TypeError, ValueError):
                price_float = 0.0
            print(f"  Price: {price_float} USD")
            print(f"  Timestamp: {current_timestamp}")

if __name__ == "__main__":
    main()
