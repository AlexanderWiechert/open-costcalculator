# filter/rds_meta.py

def extract(plan):
    for res in plan.get("resource_changes", []):
        if res.get("type") == "aws_db_instance":
            after = res.get("change", {}).get("after", {})
            return {
                "instance_class": after.get("instance_class"),
                "engine": after.get("engine"),
                "storage_gb": after.get("allocated_storage", 20),
                "multi_az": after.get("multi_az", False),
                "storage_type": after.get("storage_type", "gp2"),
            }
    return None
