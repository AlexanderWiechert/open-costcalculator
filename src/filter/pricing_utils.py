# pricing_utils.py

import json

def get_price(pricing_client, service_code, filters):
    try:
        response = pricing_client.get_products(
            ServiceCode=service_code,
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
                        return float(price)
    except Exception as e:
        print(f"⚠️ Fehler bei Preisabfrage für {service_code}: {e}")
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
            return float(prices["SpotPriceHistory"][0]["SpotPrice"])
    except Exception as e:
        print(f"⚠️ Fehler bei Spot-Preisabfrage: {e}")
    return 0.0
