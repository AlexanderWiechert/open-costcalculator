from resources.eks import ec2_filters

def test_build_filters_on_demand():
    filters = ec2_filters.build("t3.micro", "EU (Frankfurt)", "OnDemand")
    assert any(f["Field"] == "instanceType" and f["Value"] == "t3.micro" for f in filters)
    assert any(f["Field"] == "marketoption" and f["Value"] == "OnDemand" for f in filters)

def test_build_filters_spot():
    filters = ec2_filters.build("t3.micro", "EU (Frankfurt)", "Spot")
    assert any(f["Field"] == "marketoption" and f["Value"] == "Spot" for f in filters)