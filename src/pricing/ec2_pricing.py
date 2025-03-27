import boto3
import yaml
import sys
import json
import datetime
from config import REGION_MAPPING, load_config

def get_ec2_on_demand_price():
    config = load_config("config.yml")
    pricing_config = config.get("pricing", {})
    service_code = pricing_config.get("service_code", "AmazonEC2")
    region_code = pricing_config.get("region", "us-east-1")
    filters_cfg = pricing_config.get("filters", {})
    instance_type = filters_cfg.get("instance_type", "t2.micro")
    operating_system = filters_cfg.get("operating_system", "Linux")
    if operating_system == "Linux":
        operating_system = "Linux/UNIX"
    filters = [{"Type": "TERM_MATCH", "Field": "location", "Value": REGION_MAPPING.get(region_code, region_code)}]
    if instance_type:
        filters.append({"Type": "TERM_MATCH", "Field": "instanceType", "Value": instance_type})
    if operating_system:
        filters.append({"Type": "TERM_MATCH", "Field": "operatingSystem", "Value": operating_system})
    client = boto3.client("pricing", region_name="us-east-1")
    response = client.get_products(ServiceCode=service_code, Filters=filters, MaxResults=100)
    price = None
    for priceItem in response.get("PriceList", []):
        item = json.loads(priceItem)
        if "Reserved" in item.get("terms", {}):
            continue
        pre_installed = item.get("product", {}).get("attributes", {}).get("preInstalledSw", "")
        if "SQL" in pre_installed:
            continue
        capacity_status = item.get("product", {}).get("attributes", {}).get("capacitystatus", "")
        if capacity_status == "UnusedCapacityReservation":
            continue
        on_demand_terms = item.get("terms", {}).get("OnDemand", {})
        for term in on_demand_terms.values():
            price_dimensions = term.get("priceDimensions", {})
            for pd in price_dimensions.values():
                price = pd.get("pricePerUnit", {}).get("USD", "n/a")
                break
            if price is not None:
                break
        if price is not None:
            break
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return region_code, instance_type, operating_system, price, timestamp

def get_ec2_spot_price():
    config = load_config("config.yml")
    pricing_config = config.get("pricing", {})
    region_code = pricing_config.get("region", "us-east-1")
    filters_cfg = pricing_config.get("filters", {})
    instance_type = filters_cfg.get("instance_type", "t2.micro")
    operating_system = filters_cfg.get("operating_system", "Linux")
    if operating_system == "Linux":
        operating_system = "Linux/UNIX"
    ec2_client = boto3.client("ec2", region_name=region_code)
    response = ec2_client.describe_spot_price_history(
        InstanceTypes=[instance_type],
        ProductDescriptions=[operating_system],
        MaxResults=1,
        StartTime=datetime.datetime.utcnow()
    )
    price = None
    if response.get("SpotPriceHistory"):
        price = response["SpotPriceHistory"][0]["SpotPrice"]
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return region_code, instance_type, operating_system, price, timestamp

def get_ec2_price_from_config():
    config = load_config("config.yml")
    pricing_config = config.get("pricing", {})
    pricing_type = pricing_config.get("pricing_type", "on_demand").lower()
    if pricing_type == "spot":
        region, instance_type, operating_system, price, timestamp = get_ec2_spot_price()
    else:
        region, instance_type, operating_system, price, timestamp = get_ec2_on_demand_price()
    output = {
        "pricing_type": pricing_type,
        "service_code": pricing_config.get("service_code", "AmazonEC2"),
        "region": region,
        "filters": {
            "instance_type": instance_type,
            "operating_system": pricing_config.get("filters", {}).get("operating_system", "Linux")
        },
        "price": price,
        "timestamp": timestamp
    }
    return output

if __name__ == "__main__":
    output = get_ec2_price_from_config()
    print(json.dumps(output, indent=2))
