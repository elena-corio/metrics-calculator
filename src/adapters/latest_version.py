import logging
logging.basicConfig(level=logging.INFO)
from config import PROJECT_ID, SOURCE_MODEL_ID
from specklepy.api.client import SpeckleClient

def get_latest_version(client: SpeckleClient, source_model_id=None, project_id=None):
    """
    Get the latest version of a speckle model. If no versions are found, print a message and return None.
    """
    source_model_id = source_model_id or SOURCE_MODEL_ID
    project_id = project_id or PROJECT_ID
    versions = client.version.get_versions(source_model_id, project_id, limit=1)
    if not versions.items:
        logging.warning("No versions found.")
        return
    latest_version = versions.items[0]
    logging.info(f"✓ Fetching version: {latest_version.id}")
    
    return latest_version