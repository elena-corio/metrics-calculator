import json
from pathlib import Path

def load_rulebook():
    rulebook_path = Path(__file__).parent / "rulebook.json"
    with open(rulebook_path, encoding="utf-8") as f:
        return json.load(f)
