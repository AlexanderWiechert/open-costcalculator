# filter/arg_utils.py

import argparse

DEFAULT_PLAN_PATH = "../test/terraform-sf2l.plan.json"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--plan",
        default=DEFAULT_PLAN_PATH,
        help="Pfad zur terraform.plan.json Datei"
    )
    return parser.parse_args()
