import boto3
import yaml
import sys
import json
import datetime

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

def format_table(rows, header):
    # Berechne die maximale Spaltenbreite (inklusive Header)
    col_widths = [max(len(str(val)) for val in col) for col in zip(header, *rows)]

    def format_row(row):
        return "  ".join(str(val).ljust(width) for val, width in zip(row, col_widths))

    table_lines = []
    table_lines.append(format_row(header))
    table_lines.append("-" * (sum(col_widths) + 2 * (len(col_widths) - 1)))
    for row in rows:
        table_lines.append(format_row(row))

    return "\n".join(table_lines)

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

    # Der Pricing-Client läuft in us-east-1, da der Pricing-Service zentral dort betrieben wird.
    client = boto3.client('pricing', region_name='us-east-1')
    response = client.get_products(
        ServiceCode=service_code,
        Filters=filters,
        MaxResults=100
    )

    header = ["Region", "InstanceType", "OS", "Price", "PricingType", "Timestamp"]
    rows = []
    current_timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    for priceItem in response['PriceList']:
        item = json.loads(priceItem)

        # Filter: Überspringe Einträge, die Reserved-Angebote enthalten.
        if "Reserved" in item.get("terms", {}):
            continue

        product_attributes = item.get("product", {}).get("attributes", {})

        # Filter: Überspringe Einträge, bei denen preInstalledSw "SQL" enthält.
        pre_installed = product_attributes.get("preInstalledSw", "")
        if "SQL" in pre_installed:
            continue

        # Filter: Nur Einträge mit "UnusedCapacityReservation" im capacitystatus beibehalten.
        capacity_status = product_attributes.get("capacitystatus", "")
        if capacity_status != "UnusedCapacityReservation":
            continue

        # Hole die relevanten Werte
        instance_type = product_attributes.get("instanceType", "n/a")
        operating_system = product_attributes.get("operatingSystem", "n/a")

        # Extrahiere den Preis aus dem ersten OnDemand-Preis-Dimension-Eintrag
        on_demand_terms = item.get("terms", {}).get("OnDemand", {})
        price_value = None
        for term_key, term_value in on_demand_terms.items():
            price_dimensions = term_value.get("priceDimensions", {})
            for pd_key, pd_value in price_dimensions.items():
                price_value = pd_value.get("pricePerUnit", {}).get("USD", "n/a")
                break
            if price_value is not None:
                break
        if price_value is None:
            price_value = "n/a"

        rows.append([region_code, instance_type, operating_system, price_value, "on_demand", current_timestamp])

    table_output = format_table(rows, header)
    print(table_output)

if __name__ == "__main__":
    main()
