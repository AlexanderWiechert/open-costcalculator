from resources.rds import rds_filters


def test_rds_filter_generation():
    filters = rds_filters.build("db.t3.micro", "mysql", "EU (Frankfurt)", multi_az=False)
    assert any(f["Field"] == "instanceType" and f["Value"] == "db.t3.micro" for f in filters)
    assert any(f["Field"] == "databaseEngine" and f["Value"] == "mysql" for f in filters)
