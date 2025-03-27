import boto3
import yaml
import sys
import json
import datetime

def load_config(path="config.yml"):
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f)
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

    # Lese Konfigurationswerte: Region, Instanztyp und OS
    region = pricing_config.get("region", "us-east-1")
    instance_type = pricing_config.get("filters", {}).get("instance_type", "t2.micro")
    operating_system = pricing_config.get("filters", {}).get("operating_system", "Linux")
    # Falls in der config.yml "Linux" steht, erweitere ihn zu "Linux/UNIX"
    if operating_system == "Linux":
        operating_system = "Linux/UNIX"

    # Erstelle einen EC2-Client in der gewünschten Region
    client = boto3.client("ec2", region_name=region)

    # Hier erfolgt normalerweise die Logik, um Spot-Preise über boto3 abzurufen.
    # Für Demonstrationszwecke simulieren wir einen Beispielpreis:
    price = "0.023"

    # Erzeuge den aktuellen Timestamp im ISO-Format (UTC)
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # Zusammenstellen der Tabelle:
    header = ["Region", "InstanceType", "OS", "Price", "PricingType", "Timestamp"]
    rows = []
    rows.append([region, instance_type, operating_system, price, "spot", timestamp])

    table_output = format_table(rows, header)
    print(table_output)

if __name__ == "__main__":
    main()
