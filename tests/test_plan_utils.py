from core import plan_utils


def test_extract_region_from_plan_valid():
    plan = {
        "configuration": {"provider_config": {"aws": {"expressions": {"region": {"constant_value": "eu-central-1"}}}}}
    }
    assert plan_utils.extract_region_from_plan(plan) == "EU (Frankfurt)"


def test_extract_region_from_plan_invalid():
    assert plan_utils.extract_region_from_plan({}) is None
