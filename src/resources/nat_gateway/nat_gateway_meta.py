from resources.nat_gateway import nat_gateway_filter
from core import pricing_utils

def count(plan):
    return sum(
        1 for res in plan.get("resource_changes", [])
        if res.get("type") == "aws_nat_gateway"
    )

def process_nat_gateway(plan, pricing, region, hours):
    nat_count = count(plan)
    if nat_count == 0:
        return [], 0.0

    filters = nat_gateway_filter.build(region)
    unit_price = pricing_utils.get_price(pricing, "AmazonVPC", filters)
    total_price = round(unit_price * nat_count * hours, 5)

    return [[
        "NAT Gateway",
        nat_count,
        "Standard",
        f"${total_price:.5f}"
    ]], total_price
