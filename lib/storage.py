import json
from pathlib import Path
from typing import Dict

WEIGHTS_PATH = Path("data/weights.json")

def load_weights() -> Dict[str, float]:
    if WEIGHTS_PATH.exists():
        return json.loads(WEIGHTS_PATH.read_text())
    return {}

def save_weights(weights: Dict[str, float]) -> None:
    WEIGHTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    WEIGHTS_PATH.write_text(json.dumps(weights, indent=2, sort_keys=True))
