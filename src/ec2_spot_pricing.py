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
    # Setze den Startzeitpunkt 1 Stunde in der Vergangenheit
    start_time = datetime.datetime.utcnow() - datetime.timedelta(hours=1)

    response = client.describe_spot_price_history(
        InstanceTypes=[instance_type],
        ProductDescriptions=[operating_system],
        StartTime=start_time,
        MaxResults=100
    )

    results = response.get("SpotPriceHistory", [])
    if not results:
        print("Keine Spot-Preisdaten gefunden.")
        sys.exit(0)

    # Sammle alle Preiswerte und Timestamps aus den Ergebnissen
    prices = []
    timestamps = []
    for record in results:
        try:
            prices.append(float(record.get("SpotPrice", "0")))
            timestamps.append(record.get("Timestamp"))
        except ValueError:
            continue
    if not prices:
        print("Keine gültigen Preise gefunden.")
        sys.exit(0)

    # Berechne den durchschnittlichen Spotpreis über alle Ergebnisse
    overall_avg = sum(prices) / len(prices)
    # Wähle den aktuellsten Timestamp als Referenz
    latest_ts = max(timestamps) if timestamps else ""

    # Erstelle eine Tabelle mit einer einzigen Zeile für den Durchschnittspreis
    row = [region, instance_type, operating_system, f"{overall_avg:.6f}", str(latest_ts)]
    header = ["Region", "InstanceType", "ProductDescription", "Price", "Timestamp"]
    table = format_table([row], header)
    print(table)

if __name__ == "__main__":
    main()
