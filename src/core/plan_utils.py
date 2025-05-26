import pytest
import core.plan_utils as plan_utils
def test_extract_region_from_plan_valid():
    plan = {
        "configuration": {
            "provider_config": {
                "aws": {
                    "expressions": {
                        "region": {
                            "constant_value": "eu-central-1"
                        }
                    }
                }
            }
        }
    }
    assert plan_utils.extract_region_from_plan(plan) == "eu-central-1"

def test_extract_region_from_plan_invalid(caplog):
    # Kein 'region'-Key enthalten
    plan = {}

    with caplog.at_level("WARNING"):
        result = plan_utils.extract_region_from_plan(plan)

    assert result is None
    assert "Region konnte aus dem Plan nicht extrahiert werden." in caplog.text

def extract_region_from_plan(plan: dict) -> str | None:
    try:
        return plan["configuration"]["provider_config"]["aws"]["expressions"]["region"]["constant_value"]
    except KeyError:
        return None
