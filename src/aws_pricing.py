import boto3
import yaml
import sys
import json

# Mapping von Region-Codes zu AWS Pricing "location"-Werten
REGION_MAPPING = {
    "us-east-1": "US East (N. Virginia)",
    "us-east-2": "US East (Ohio)",
    "us-west-1": "US West (N. California)",
    "us-west-2": "US West (Oregon)",
    "af-south-1": "Africa (Cape Town)",
    "ap-east-1": "Asia Pacific (Hong Kong)",
    "ap-south-1": "Asia Pacific (Mumbai)",
    "ap-northeast-1": "Asia Pacific (Tokyo)",
    "ap-northeast-2": "Asia Pacific (Seoul)",
    "ap-northeast-3": "Asia Pacific (Osaka)",
    "ap-southeast-1": "Asia Pacific (Singapore)",
    "ap-southeast-2": "Asia Pacific (Sydney)",
    "ca-central-1": "Canada (Central)",
    "eu-central-1": "EU (Frankfurt)",
    "eu-west-1": "EU (Ireland)",
    "eu-west-2": "EU (London)",
    "eu-west-3": "EU (Paris)",
    "eu-north-1": "EU (Stockholm)",
    "eu-south-1": "EU (Milan)",
    "me-south-1": "Middle East (Bahrain)",
    "sa-east-1": "South America (São Paulo)"
}

def load_config(path="config.yml"):
    try:
        with open(path, "r") as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"Fehler beim Laden der Konfiguration: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    config = load_config()

    pricing_config = config.get("pricing", {})
    service_code = pricing_config.get("service_code", "AmazonEC2")

    region_code = pricing_config.get("region", "us-east-1")
    location_filter_value = REGION_MAPPING.get(region_code, region_code)

    filters = []
    filters.append({
        "Type": "TERM_MATCH",
        "Field": "location",
        "Value": location_filter_value
    })

    filters_cfg = pricing_config.get("filters", {})
    if "instance_type" in filters_cfg:
        filters.append({
            "Type": "TERM_MATCH",
            "Field": "instanceType",
            "Value": filters_cfg["instance_type"]
        })
    if "operating_system" in filters_cfg:
        filters.append({
            "Type": "TERM_MATCH",
            "Field": "operatingSystem",
            "Value": filters_cfg["operating_system"]
        })

    # Der Pricing-Client läuft immer in us-east-1, da der Pricing-Service dort zentral ist.
    client = boto3.client('pricing', region_name='us-east-1')
    response = client.get_products(
        ServiceCode=service_code,
        Filters=filters,
        MaxResults=100
    )

    # Entferne den Debug-Output, damit nur gültiges JSON ausgegeben wird.
    for priceItem in response['PriceList']:
        item = json.loads(priceItem)
        item['region_code'] = region_code
        print(json.dumps(item))

if __name__ == "__main__":
    main()
