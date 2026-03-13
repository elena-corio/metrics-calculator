import logging
from typing import Optional
logging.basicConfig(level=logging.INFO)

from specklepy.api.client import SpeckleClient
from specklepy.core.api.inputs.model_inputs import CreateModelInput


def get_models_in_project(client: SpeckleClient, project_id: str) -> list:
    """
    Fetch all models in a project.
    
    Args:
        client: Authenticated SpeckleClient instance
        project_id: The ID of the Speckle project
        
    Returns:
        List of model objects
    """
    models = client.model.get_models(project_id=project_id)
    return models.items


def find_metrics_model(models: list) -> Optional[str]:
    """
    Find the first model named 'metrics' (case-insensitive).
    
    Handles both:
    - Flat names: "metrics"
    - Folder paths: "data/metrics", "folder/subfolder/metrics"
    
    Args:
        models: List of model objects from Speckle
        
    Returns:
        Model ID if found, None otherwise
    """
    for model in models:
        model_name = model.name.lower()
        # Check if name is exactly "metrics" or ends with "/metrics"
        if model_name == "metrics" or model_name.endswith("/metrics"):
            logging.info(f"✓ Found existing metrics model: {model.id} (name: {model.name})")
            return model.id
    return None


def create_metrics_model(client: SpeckleClient, project_id: str) -> str:
    """
    Create a new model named 'data/metrics' in the project.
    
    This will appear in the Speckle UI under the 'data' folder.
    
    Args:
        client: Authenticated SpeckleClient instance
        project_id: The ID of the Speckle project
        
    Returns:
        The ID of the newly created model
    """
    model_input = CreateModelInput(
        name="data/metrics",
        description="Automated metrics calculation results",
        project_id=project_id
    )
    new_model = client.model.create(model_input)
    logging.info(f"✓ Created new metrics model: {new_model.id} (name: data/metrics)")
    return new_model.id


def get_or_create_metrics_model(client: SpeckleClient, project_id: str) -> str:
    """
    Get the metrics model ID if it exists, otherwise create it.
    
    This function:
    1. Fetches all models in the project
    2. Searches for a model named 'metrics' or ending with '/metrics' (e.g., 'data/metrics')
    3. Returns the existing model ID if found
    4. Creates a new 'data/metrics' model if not found
    
    Args:
        client: Authenticated SpeckleClient instance
        project_id: The ID of the Speckle project
        
    Returns:
        The ID of the metrics model (existing or newly created)
    """
    models = get_models_in_project(client, project_id)
    
    metrics_model_id = find_metrics_model(models)
    
    if metrics_model_id:
        return metrics_model_id
    
    return create_metrics_model(client, project_id)
