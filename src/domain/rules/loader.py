"""
Load from JSON files.
"""

import json
from pathlib import Path

def load_rulebook():
    """
    Load the rulebook from a JSON file located in the same directory as this script.
    """
    rulebook_path = Path(__file__).parent / "rulebook.json"
    with open(rulebook_path, encoding="utf-8") as f:
        return json.load(f)