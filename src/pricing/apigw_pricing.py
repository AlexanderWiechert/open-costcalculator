import boto3
import json

def query_apigw_price(api_type="REST"):
    pricing_client = boto3.client("pricing", region_name="us-east-1")
    response = pricing_client.get_products(
        ServiceCode="AmazonAPIGateway",
        Filters=[
            {"Type": "TERM_MATCH", "Field": "apiType", "Value": api_type}
        ],
        MaxResults=1
    )
    return response

def extract_price_from_apigw_response(response):
    price = None
    price_list = response.get("PriceList", [])
    if price_list:
        item = json.loads(price_list[0])
        terms = item.get("terms", {}).get("OnDemand", {})
        for term in terms.values():
            dimensions = term.get("priceDimensions", {})
            for pd in dimensions.values():
                price = pd.get("pricePerUnit", {}).get("USD")
                if price is not None:
                    break
            if price is not None:
                break
    return price
