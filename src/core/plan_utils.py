# filter/plan_utils.py

import json
from pathlib import Path

from core import logger


def extract_plan(path):
    plan_path = Path(path)
    if not plan_path.is_file():
        logger.error(f"Die angegebene Datei '{path}' wurde nicht gefunden.")
        return None

    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Fehler beim Einlesen der Plan-Datei: {e}")
        return None
