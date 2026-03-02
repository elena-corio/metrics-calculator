import logging
logging.basicConfig(level=logging.INFO)
from config import PROJECT_ID, SOURCE_MODEL_ID
from specklepy.api.client import SpeckleClient

def get_latest_version(client: SpeckleClient):
    """
    Get the latest version of a speckle model. If no versions are found, print a message and return None.
    """
    versions = client.version.get_versions(SOURCE_MODEL_ID, PROJECT_ID, limit=1)
    if not versions.items:
        logging.warning("No versions found.")
        return
    latest_version = versions.items[0]
    logging.info(f"✓ Fetching version: {latest_version.id}")
    
    return latest_version