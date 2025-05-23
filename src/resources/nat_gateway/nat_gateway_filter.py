# filter/nat_gateway_filter.py

# Standardfilter zur Preisabfrage für NAT Gateway
# https://aws.amazon.com/de/vpc/pricing/

def build(region_name):
    return [
        {"Type": "TERM_MATCH", "Field": "productFamily", "Value": "NAT Gateway"},
        {"Type": "TERM_MATCH", "Field": "location", "Value": region_name},
        {"Type": "TERM_MATCH", "Field": "usagetype", "Value": "NatGateway-Hours"}
    ]
