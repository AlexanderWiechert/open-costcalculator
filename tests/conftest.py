import sys
from pathlib import Path

# src/ zum sys.path hinzufügen
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
