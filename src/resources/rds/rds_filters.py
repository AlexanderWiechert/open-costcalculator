# resources/rds/rds_filters.py


def build(instance_class, engine, location, multi_az=False):
    """
    Baut die Pricing API Filter für eine RDS Instanz.
    """
    filters = [
        {"Type": "TERM_MATCH", "Field": "instanceType", "Value": instance_class},
        {"Type": "TERM_MATCH", "Field": "databaseEngine", "Value": engine},
        {"Type": "TERM_MATCH", "Field": "location", "Value": location},
        {"Type": "TERM_MATCH", "Field": "deploymentOption", "Value": "Multi-AZ" if multi_az else "Single-AZ"},
    ]
    return filters
