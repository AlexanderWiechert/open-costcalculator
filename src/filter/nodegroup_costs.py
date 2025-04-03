# filter/nodegroup_costs.py

from . import ec2_filters, pricing_utils, pricing_defaults

def calculate_nodegroup_costs(pricing, ec2_client, instance_type, desired_size, marketoption, region, hours_per_month):
    ec2 = ec2_filters.build(instance_type, region, marketoption)
    if marketoption == "OnDemand":
        ec2_unit_cost = pricing_utils.get_price(pricing, "AmazonEC2", ec2)
    else:
        ec2_unit_cost = pricing_utils.get_spot_price(ec2_client, instance_type)

    ec2_cost = round(ec2_unit_cost * desired_size * hours_per_month, 5)

    ebs_price_per_gb = pricing_defaults.EBS_STORAGE_PRICING.get("gp3", 0.08)
    ebs_cost = round((ebs_price_per_gb * 20 / 730) * desired_size * hours_per_month, 5)

    rows = [
        ["Node Group (EC2)", desired_size, instance_type, f"${ec2_cost:.5f}"],
        ["EBS Volumes", desired_size, "gp3 (20 GB)", f"${ebs_cost:.5f}"]
    ]
    return rows, ec2_cost + ebs_cost
