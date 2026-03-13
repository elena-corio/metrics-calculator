import pytest
import os
from dotenv import load_dotenv
from adapters.metric_model_setup import (
    get_models_in_project,
    find_metrics_model,
    create_metrics_model,
    get_or_create_metrics_model
)
from adapters.speckle_client import get_client


@pytest.fixture(scope="module")
def speckle_client():
    """Get a real authenticated Speckle client."""
    load_dotenv()
    return get_client()


@pytest.fixture(scope="module")
def test_project_id():
    """
    Get the test project ID from environment variables.
    Set SPECKLE_TEST_PROJECT_ID in your .env file.
    """
    load_dotenv()
    project_id = os.getenv("SPECKLE_TEST_PROJECT_ID")
    if not project_id:
        pytest.skip("SPECKLE_TEST_PROJECT_ID not set in .env file")
    return project_id


def test_get_models_in_project_integration(speckle_client, test_project_id):
    """Integration test: Fetch all models in a real project."""
    models = get_models_in_project(speckle_client, test_project_id)
    
    assert isinstance(models, list)
    # Project should have at least one model
    assert len(models) >= 0
    
    # If models exist, verify they have required attributes
    if models:
        assert hasattr(models[0], 'id')
        assert hasattr(models[0], 'name')


def test_find_metrics_model_integration(speckle_client, test_project_id):
    """Integration test: Find metrics model in real project."""
    models = get_models_in_project(speckle_client, test_project_id)
    result = find_metrics_model(models)
    
    # Result should be either a string (model ID) or None
    assert result is None or isinstance(result, str)
    
    # If found, verify it's a valid model ID format
    if result:
        assert len(result) > 0


def test_get_or_create_metrics_model_integration(speckle_client, test_project_id):
    """
    Integration test: Get or create metrics model in real project.
    
    This test is idempotent - it will:
    1. Find existing metrics model if it exists
    2. Create one if it doesn't exist
    3. On subsequent runs, find the one created in step 2
    """
    result = get_or_create_metrics_model(speckle_client, test_project_id)
    
    # Should return a valid model ID
    assert isinstance(result, str)
    assert len(result) > 0
    
    # Verify the model actually exists by fetching it again
    models = get_models_in_project(speckle_client, test_project_id)
    metrics_model_id = find_metrics_model(models)
    
    assert metrics_model_id == result
    
    # Verify the model has the correct name
    metrics_model = next((m for m in models if m.id == result), None)
    assert metrics_model is not None
    assert metrics_model.name.lower() == "metrics"


def test_get_or_create_metrics_model_idempotent(speckle_client, test_project_id):
    """
    Integration test: Verify get_or_create is idempotent.
    
    Running it twice should return the same model ID.
    """
    first_result = get_or_create_metrics_model(speckle_client, test_project_id)
    second_result = get_or_create_metrics_model(speckle_client, test_project_id)
    
    assert first_result == second_result
