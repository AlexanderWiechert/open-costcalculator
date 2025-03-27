import yaml
import sys
import subprocess

def load_config(path="config.yml"):
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Fehler beim Laden der Konfiguration: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    config = load_config()
    pricing_config = config.get("pricing", {})
    pricing_type = pricing_config.get("pricing_type", "on_demand").lower()

    if pricing_type == "on_demand":
        subprocess.run(["python", "ec2_on_demand_pricing.py"])
    elif pricing_type == "spot":
        subprocess.run(["python", "ec2_spot_pricing.py"])
    else:
        print(f"Unbekannter pricing_type: {pricing_type}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
