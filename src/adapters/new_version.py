import logging
logging.basicConfig(level=logging.INFO)
from config import PROJECT_ID, TARGET_MODEL_ID
from specklepy.core.api.inputs.version_inputs import CreateVersionInput
from specklepy.core.api.inputs.model_inputs import CreateModelInput
from specklepy.api.client import SpeckleClient

def create_version(client: SpeckleClient, object_id):
    # Create a version
    version_input = CreateVersionInput(
        project_id=PROJECT_ID,
        model_id=TARGET_MODEL_ID,
        object_id=object_id,
    )
    version = client.version.create(version_input)

    logging.info(f"✓ Created version: {version.id}")
