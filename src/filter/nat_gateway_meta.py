# filter/nat_gateway_meta.py

def count(plan):
    """
    Zählt die Anzahl der NAT Gateways im Terraform Plan.

    :param plan: Eingeladener Terraform Plan (JSON-Dict)
    :return: Anzahl der Ressourcen vom Typ aws_nat_gateway
    """
    count = 0
    for res in plan.get("resource_changes", []):
        if res.get("type") == "aws_nat_gateway":
            count += 1
    return count
