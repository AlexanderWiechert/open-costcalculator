# filter/rds_filters.py

def build(instance_class, engine, region_name, multi_az=False):
    return [
        {"Type": "TERM_MATCH", "Field": "instanceType", "Value": instance_class},
        {"Type": "TERM_MATCH", "Field": "databaseEngine", "Value": engine},
        {"Type": "TERM_MATCH", "Field": "location", "Value": region_name},
        {"Type": "TERM_MATCH", "Field": "deploymentOption", "Value": "Multi-AZ" if multi_az else "Single-AZ"}
    ]
