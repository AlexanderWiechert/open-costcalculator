import json
import boto3
import datetime

REGION_MAPPING = {
    "us-east-1": "US East (N. Virginia)",
    "us-east-2": "US East (Ohio)",
    "us-west-1": "US West (N. California)",
    "us-west-2": "US West (Oregon)",
    "eu-central-1": "EU (Frankfurt)"
}

def query_on_demand_price(instance_type, region, marketoption, operating_system="Linux", pre_installed_sw="NA"):
    pricing_client = boto3.client("pricing", region_name="us-east-1")
    location = REGION_MAPPING.get(region, region)
    response = pricing_client.get_products(
        ServiceCode="AmazonEC2",
        Filters=[
            {"Type": "TERM_MATCH", "Field": "location", "Value": location},
            {"Type": "TERM_MATCH", "Field": "instanceType", "Value": instance_type},
            {"Type": "TERM_MATCH", "Field": "operatingSystem", "Value": operating_system},
            {"Type": "TERM_MATCH", "Field": "preInstalledSw", "Value": pre_installed_sw},
            {"Type": "TERM_MATCH", "Field": "marketoption", "Value": marketoption},
            {"Type": "TERM_MATCH", "Field": "tenancy", "Value": "Shared"}
        ],
        MaxResults=1
    )
    return response

def query_spot_price(instance_type, region, operating_system="Linux/UNIX"):
    ec2_client = boto3.client("ec2", region_name=region)
    response = ec2_client.describe_spot_price_history(
        InstanceTypes=[instance_type],
        ProductDescriptions=[operating_system],
        MaxResults=1,
        StartTime=datetime.datetime.utcnow()
    )
    if response.get("SpotPriceHistory"):
        return response["SpotPriceHistory"][0]["SpotPrice"]
    return None

def extract_price_from_on_demand_response(response):
    price = None
    price_list = response.get("PriceList", [])
    if price_list:
        item = json.loads(price_list[0])
        on_demand_terms = item.get("terms", {}).get("OnDemand", {})
        for term in on_demand_terms.values():
            price_dimensions = term.get("priceDimensions", {})
            for pd in price_dimensions.values():
                price = pd.get("pricePerUnit", {}).get("USD")
                if price is not None:
                    break
            if price is not None:
                break
    return price

def load_tf_plan(filename):
    with open(filename, "r") as f:
        return json.load(f)

def extract_variables(plan):
    vars_extracted = {}
    variables = plan.get("variables", {})
    for var_name, var_content in variables.items():
        vars_extracted[var_name] = var_content.get("value")
    return vars_extracted

def extract_cost_info(plan):
    cost_info = []
    for resource in plan.get("resource_changes", []):
        if resource.get("type") == "aws_eks_node_group":
            change = resource.get("change", {})
            after = change.get("after", {})
            instance_types = after.get("instance_types", [])
            capacity_type = after.get("capacity_type")
            cluster_name = after.get("cluster_name")
            scaling_config = after.get("scaling_config", [])
            desired_size = None
            if scaling_config and isinstance(scaling_config, list):
                config = scaling_config[0]
                desired_size = config.get("desired_size")
            cost_info.append({
                "resource": resource.get("address"),
                "instance_types": instance_types,
                "capacity_type": capacity_type,
                "cluster_name": cluster_name,
                "desired_size": desired_size
            })
    return cost_info

def main():
    plan = load_tf_plan("plans/eks.json")
    variables = extract_variables(plan)
    region = variables.get("region", "us-east-1")
    cost_info = extract_cost_info(plan)

    print("Extracted Variables:")
    print(json.dumps(variables, indent=2))

    print("\nSummary of cost-relevant resources and hourly cost calculation:")
    current_timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    for info in cost_info:
        print(f"\nResource (eks_node_group): {info['resource']}")
        print(f"  Cluster Name: {info['cluster_name']}")
        print(f"  Capacity Type: {info['capacity_type']}")
        if info.get("desired_size") is not None:
            print(f"  Number of Instances: {info['desired_size']}")
        else:
            print("  Number of Instances: not defined")
        for instance_type in info["instance_types"]:
            if info["capacity_type"].upper() == "SPOT":
                price = query_spot_price(instance_type, region)
            else:
                # Der marketoption filter wird aus dem Plan abgeleitet
                marketoption = "OnDemand" if info["capacity_type"].upper() == "ON_DEMAND" else info["capacity_type"]
                response = query_on_demand_price(instance_type, region, marketoption)
                price = extract_price_from_on_demand_response(response)
            try:
                price_float = float(price)
            except (TypeError, ValueError):
                price_float = 0.0
            if info.get("desired_size") is not None:
                hourly_cost = price_float * info["desired_size"]
            else:
                hourly_cost = price_float
            print(f"  Instance Type: {instance_type}")
            print(f"  Hourly Cost: {hourly_cost} USD/h")
            print(f"  Timestamp: {current_timestamp}")

if __name__ == "__main__":
    main()
