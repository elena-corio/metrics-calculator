"""
Integration tests for model validation logic using real Speckle models.
"""

import pytest
import os
from dotenv import load_dotenv
from specklepy.api import operations
from specklepy.transports.server import ServerTransport

from adapters.validators import validate_model_structure, ValidationResult
from adapters.speckle_client import get_client
from adapters.latest_version import get_latest_version
from config import REQUIRED_COLLECTIONS, COLLECTION_PROPERTY_REQUIREMENTS


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


@pytest.fixture(scope="module")
def test_source_model_id():
    """
    Get the test source model ID from environment variables.
    Set SPECKLE_TEST_SOURCE_MODEL_ID in your .env file.
    """
    load_dotenv()
    model_id = os.getenv("SPECKLE_TEST_SOURCE_MODEL_ID")
    
    if not model_id:
        pytest.skip("SPECKLE_TEST_SOURCE_MODEL_ID not set in .env file")
    return model_id


@pytest.fixture(scope="module")
def speckle_model_data(speckle_client, test_project_id, test_source_model_id):
    """
    Fetch actual Speckle model data from the test project.
    This returns the actual data object with collections.
    """
    # Get latest version
    version = get_latest_version(
        speckle_client, 
        source_model_id=test_source_model_id,
        project_id=test_project_id
    )
    
    if not version:
        pytest.skip("No versions found in test model")
    
    # Create transport and receive data
    transport = ServerTransport(stream_id=test_project_id, client=speckle_client)
    
    # Check if version has referenced_object or referencedObject
    if hasattr(version, 'referenced_object'):
        object_id = version.referenced_object
    elif hasattr(version, 'referencedObject'):
        object_id = version.referencedObject
    else:
        pytest.skip("Version has no referenced object")
    
    # Receive the actual data
    data = operations.receive(object_id, transport)
    
    return data


class TestRealSpeckleModelValidation:
    """Test validation with real Speckle models."""
    
    def test_validate_real_speckle_model(self, speckle_model_data):
        """Integration test: Validate a real Speckle model structure."""
        result = validate_model_structure(
            speckle_model_data,
            REQUIRED_COLLECTIONS,
            COLLECTION_PROPERTY_REQUIREMENTS
        )
        
        # Print result for debugging
        print(f"\nValidation Result:")
        print(f"  Valid: {result.is_valid}")
        print(f"  Code: {result.code}")
        print(f"  Message: {result.message}")
        if result.details:
            print(f"  Details: {result.details}")
        
        # The model should either pass or fail with clear error codes
        assert result.code in [
            "VALID",
            "MISSING_COLLECTIONS",
            "MISSING_PROPERTIES",
            "NO_PROPERTIES_ATTRIBUTE",
            "NULL_PROPERTIES",
            "NO_ELEMENTS_ATTRIBUTE",
            "INVALID_ELEMENTS_STRUCTURE"
        ]
        
        # If invalid, details should be provided
        if not result.is_valid:
            assert result.details is not None
            assert len(result.message) > 0
    
    def test_model_has_elements_attribute(self, speckle_model_data):
        """Verify the real model has the expected elements structure."""
        assert hasattr(speckle_model_data, 'elements')
        assert speckle_model_data.elements is not None
    
    def test_model_collections_structure(self, speckle_model_data):
        """Verify collections in the real model have expected structure."""
        if hasattr(speckle_model_data, 'elements'):
            collections = speckle_model_data.elements
            
            # Print available collections for debugging
            collection_names = [col.name for col in collections]
            print(f"\nAvailable collections: {collection_names}")
            
            # Each collection should have name and elements
            for collection in collections:
                assert hasattr(collection, 'name')
                assert hasattr(collection, 'elements')


class TestValidationResultStructure:
    """Test ValidationResult data structure."""
    
    def test_validation_result_has_required_fields(self, speckle_model_data):
        """Validation result should have all required fields."""
        result = validate_model_structure(
            speckle_model_data,
            REQUIRED_COLLECTIONS,
            COLLECTION_PROPERTY_REQUIREMENTS
        )
        
        assert hasattr(result, 'is_valid')
        assert hasattr(result, 'message')
        assert hasattr(result, 'code')
        assert isinstance(result.is_valid, bool)
        assert isinstance(result.message, str)
        assert isinstance(result.code, str)
    
    def test_validation_result_to_dict(self, speckle_model_data):
        """ValidationResult should convert to dict for Automate."""
        result = validate_model_structure(
            speckle_model_data,
            REQUIRED_COLLECTIONS,
            COLLECTION_PROPERTY_REQUIREMENTS
        )
        
        result_dict = result.to_dict()
        
        assert isinstance(result_dict, dict)
        assert 'code' in result_dict
        assert result_dict['code'] == result.code


class TestCollectionPropertyValidation:
    """Test property validation on real model collections."""
    
    def test_check_required_collections_present(self, speckle_model_data):
        """Check which required collections are present in the model."""
        if not hasattr(speckle_model_data, 'elements'):
            pytest.skip("Model has no elements attribute")
        
        existing_collections = [col.name for col in speckle_model_data.elements]
        print(f"\nRequired collections: {REQUIRED_COLLECTIONS}")
        print(f"Existing collections: {existing_collections}")
        
        missing = [col for col in REQUIRED_COLLECTIONS if col not in existing_collections]
        if missing:
            print(f"Missing collections: {missing}")
    
    def test_check_properties_on_elements(self, speckle_model_data):
        """Check if elements in collections have required properties."""
        if not hasattr(speckle_model_data, 'elements'):
            pytest.skip("Model has no elements attribute")
        
        for collection in speckle_model_data.elements:
            if collection.name not in REQUIRED_COLLECTIONS:
                continue
            
            if not collection.elements:
                print(f"\n{collection.name}: Empty collection (no elements)")
                continue
            
            sample = collection.elements[0]
            required_props = COLLECTION_PROPERTY_REQUIREMENTS.get(collection.name, [])
            
            print(f"\n{collection.name}:")
            print(f"  Has properties attr: {hasattr(sample, 'properties')}")
            
            if hasattr(sample, 'properties') and sample.properties:
                existing_props = list(sample.properties.keys()) if hasattr(sample.properties, 'keys') else []
                missing_props = [p for p in required_props if p not in existing_props]
                
                print(f"  Required: {required_props}")
                print(f"  Existing: {existing_props}")
                if missing_props:
                    print(f"  Missing: {missing_props}")


class TestValidationErrorCodes:
    """Test that validation returns appropriate error codes."""
    
    def test_error_codes_are_descriptive(self, speckle_model_data):
        """Validation error codes should be clear and actionable."""
        result = validate_model_structure(
            speckle_model_data,
            REQUIRED_COLLECTIONS,
            COLLECTION_PROPERTY_REQUIREMENTS
        )
        
        # Valid codes
        valid_codes = [
            "VALID",
            "MISSING_COLLECTIONS",
            "MISSING_PROPERTIES",
            "NO_PROPERTIES_ATTRIBUTE",
            "NULL_PROPERTIES",
            "NO_ELEMENTS_ATTRIBUTE",
            "INVALID_ELEMENTS_STRUCTURE"
        ]
        
        assert result.code in valid_codes, f"Unexpected code: {result.code}"
    
    def test_failed_validation_includes_details(self, speckle_model_data):
        """If validation fails, details should explain what's wrong."""
        result = validate_model_structure(
            speckle_model_data,
            REQUIRED_COLLECTIONS,
            COLLECTION_PROPERTY_REQUIREMENTS
        )
        
        if not result.is_valid:
            assert result.details is not None
            assert isinstance(result.details, dict)
            assert len(result.details) > 0
            
            # Details should contain useful information
            if result.code == "MISSING_COLLECTIONS":
                assert "missing" in result.details
                assert isinstance(result.details["missing"], list)
            
            elif result.code == "MISSING_PROPERTIES":
                assert "collection" in result.details
                assert "missing_properties" in result.details
