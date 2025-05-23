from core import arg_utils

def test_default_plan_path():
    assert arg_utils.DEFAULT_PLAN_PATH.endswith(".json")
