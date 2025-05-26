import json

from core import arg_utils, logger


def get_price_for_service(
    pricing_client, service_code: str, filters: list, unit: str = "Hrs", fallback_price: float = 0.0
) -> float:
    try:
        response = pricing_client.get_products(ServiceCode=service_code, Filters=filters, MaxResults=1)
        for item in response.get("PriceList", []):
            offer = json.loads(item)
            terms = offer.get("terms", {}).get("OnDemand", {})
            for term in terms.values():
                dimensions = term.get("priceDimensions", {})
                for dim in dimensions.values():
                    if dim.get("unit") == unit:
                        price = dim.get("pricePerUnit", {}).get("USD")
                        if price:
                            if arg_utils.LOG_DEBUG:  # 💡 Nur wenn --debug
                                logger.info(
                                    f"🔍 Gefundener Preis: {price} USD für Service {service_code} mit Filtern {filters}"
                                )
                            return float(price)
    except Exception as e:
        logger.warn(f"Fehler bei Preisabfrage für {service_code}: {e}")
    return fallback_price


def get_spot_price(ec2_client, instance_type: str, availability_zone: str = "eu-central-1a") -> float:
    try:
        prices = ec2_client.describe_spot_price_history(
            InstanceTypes=[instance_type],
            ProductDescriptions=["Linux/UNIX"],
            AvailabilityZone=availability_zone,
            MaxResults=1,
        )
        if prices.get("SpotPriceHistory"):
            price = float(prices["SpotPriceHistory"][0]["SpotPrice"])
            if arg_utils.LOG_DEBUG:  # 💡 Auch hier!
                logger.info(f"☁️  Spotpreis {instance_type} in {availability_zone}: ${price:.4f} USD")
            return price
    except Exception as e:
        logger.warn(f"Fehler bei Spot-Preisabfrage: {e}")
    return 0.0


def get_nat_gateway_price(pricing_client, filters: list) -> float:
    """
    Gibt dynamischen Preis für NAT Gateway zurück (basierend auf Stunden).
    """
    return get_price_for_service(
        pricing_client=pricing_client, service_code="AmazonVPC", filters=filters, unit="Hrs", fallback_price=0.045
    )
