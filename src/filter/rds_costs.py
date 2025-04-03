# filter/rds_costs.py

from . import rds_filters, rds_utils, pricing_utils, pricing_defaults

def calculate_rds_cost(pricing_client, plan, region, hours_per_month):
    from . import logger  # lazy import to avoid circular import

    modules = [plan["planned_values"]["root_module"]]
    while modules:
        module = modules.pop()
        for res in module.get("resources", []):
            if res.get("type") == "aws_db_instance":
                values = res.get("values", {})
                instance_class = values.get("instance_class")
                engine = values.get("engine")
                storage_type = values.get("storage_type")
                storage_gb = values.get("allocated_storage")
                multi_az = values.get("multi_az", False)

                rds_filter = rds_filters.build(instance_class, engine, region, multi_az)
                instance_price = pricing_utils.get_price(pricing_client, "AmazonRDS", rds_filter)
                storage_price = rds_utils.get_rds_storage_price(pricing_client, storage_type, region)

                instance_cost = round(instance_price * hours_per_month, 5)
                storage_cost = round(storage_price * storage_gb, 5)

                return [
                    ["RDS Instance", 1, instance_class, f"${instance_cost:.5f}"],
                    ["RDS Storage", storage_gb, storage_type, f"${storage_cost:.5f}"]
                ], instance_cost + storage_cost
        modules.extend(module.get("child_modules", []))
    return [], 0.0
