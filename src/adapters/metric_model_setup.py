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


def find_metrics_model(models: list, metrics_model_name: str = "data/metrics") -> Optional[str]:
    """
    Find the first model matching the specified name (case-insensitive).
    
    Handles both:
    - Flat names: "metrics"
    - Folder paths: "data/metrics", "folder/subfolder/metrics"
    
    Args:
        models: List of model objects from Speckle
        metrics_model_name: Name of the metrics model to search for (default: "data/metrics")
        
    Returns:
        Model ID if found, None otherwise
    """
    # Extract the base name from the path (e.g., "metrics" from "data/metrics")
    base_name = metrics_model_name.split("/")[-1].lower()
    target_name = metrics_model_name.lower()
    
    for model in models:
        model_name = model.name.lower()
        # Check if name matches exactly or ends with the base name
        if model_name == target_name or model_name == base_name or model_name.endswith(f"/{base_name}"):
            logging.info(f"✓ Found existing metrics model: {model.id} (name: {model.name})")
            return model.id
    return None


def create_metrics_model(client: SpeckleClient, project_id: str, metrics_model_name: str = "data/metrics") -> str:
    """
    Create a new metrics model in the project.
    
    If the name contains '/', it will appear in the Speckle UI organized in folders.
    For example, 'data/metrics' will appear under the 'data' folder.
    
    Args:
        client: Authenticated SpeckleClient instance
        project_id: The ID of the Speckle project
        metrics_model_name: Name for the metrics model (default: "data/metrics")
        
    Returns:
        The ID of the newly created model
    """
    model_input = CreateModelInput(
        name=metrics_model_name,
        description="Automated metrics calculation results",
        project_id=project_id
    )
    new_model = client.model.create(model_input)
    logging.info(f"✓ Created new metrics model: {new_model.id} (name: {metrics_model_name})")
    return new_model.id


def get_or_create_metrics_model(client: SpeckleClient, project_id: str, metrics_model_name: str = "data/metrics") -> str:
    """
    Get the metrics model ID if it exists, otherwise create it.
    
    This function:
    1. Fetches all models in the project
    2. Searches for a model matching the specified name
    3. Returns the existing model ID if found
    4. Creates a new model with the specified name if not found
    
    Args:
        client: Authenticated SpeckleClient instance
        project_id: The ID of the Speckle project
        metrics_model_name: Name for the metrics model (default: "data/metrics")
        
    Returns:
        The ID of the metrics model (existing or newly created)
    """
    models = get_models_in_project(client, project_id)
    
    metrics_model_id = find_metrics_model(models, metrics_model_name)
    
    if metrics_model_id:
        return metrics_model_id
    
    return create_metrics_model(client, project_id, metrics_model_name)
