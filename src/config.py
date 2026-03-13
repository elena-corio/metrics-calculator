"""
Load configuration from environment variables
"""
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

WORKSPACE_ID = os.getenv("SPECKLE_WORKSPACE_ID", "a1cd06bae2")
PROJECT_ID = os.getenv("SPECKLE_PROJECT_ID", "dcca94731b")
SOURCE_MODEL_ID = os.getenv("SPECKLE_SOURCE_MODEL_ID", "827526cd48")
TARGET_MODEL_ID = os.getenv("SPECKLE_TARGET_MODEL_ID", "a17c364985")
METRICS_MODEL_NAME = os.getenv("SPECKLE_METRICS_MODEL_NAME", "data/metrics")

AUTHORS = ["Elena Corio, Symon Kipkemei"]
FUNCTION = "digital-tissue-automate"

# Validation Configuration
REQUIRED_COLLECTIONS = [
    "COLUMNS", "CORES", "FACADES", 
    "OPEN_SPACES", "SLABS", "UNITS", "VOLUMES"
]

COLLECTION_PROPERTY_REQUIREMENTS = {
    "COLUMNS": ["cluster_id", "level", "material", "section", "size", "thickness"],
    "CORES": ["cluster_id", "level", "material", "section", "size", "thickness"],
    "FACADES": ["cluster_id", "level", "material", "thickness", "enclosed_volume"],
    "SLABS": ["cluster_id", "level", "material", "thickness"],
    "UNITS": ["cluster_id", "level", "program"],
    "OPEN_SPACES": ["cluster_id", "level"],
    "VOLUMES": ["cluster_id", "level"],
}