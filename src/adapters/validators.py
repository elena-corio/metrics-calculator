"""
Validation logic for Speckle model structure and properties.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Any


@dataclass
class ValidationResult:
    """Result of model validation."""
    is_valid: bool
    message: str
    code: str
    details: Optional[Dict] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for Automate results."""
        result = {"code": self.code}
        if self.details:
            result.update(self.details)
        return result


def validate_model_structure(
    data: Any,
    required_collections: List[str],
    property_requirements: Dict[str, List[str]]
) -> ValidationResult:
    """
    Validate that model has required collections and properties.
    
    Args:
        data: Speckle data object with elements
        required_collections: List of collection names that must exist
        property_requirements: Dict mapping collection names to required property keys
    
    Returns:
        ValidationResult with validation status and details
    """
    # Check if data has elements attribute
    if not hasattr(data, 'elements'):
        return ValidationResult(
            is_valid=False,
            message="Requirements not met: Model data has no 'elements' attribute",
            code="NO_ELEMENTS_ATTRIBUTE",
            details={"error": "Data object missing 'elements' attribute"}
        )
    
    # Extract collection names from data
    try:
        existing_collections = [collection.name for collection in data.elements]
    except (AttributeError, TypeError) as e:
        return ValidationResult(
            is_valid=False,
            message=f"Requirements not met: Cannot read collection names from elements",
            code="INVALID_ELEMENTS_STRUCTURE",
            details={"error": str(e)}
        )
    
    # Phase 1: Validate required collections exist
    missing_collections = [
        col for col in required_collections 
        if col not in existing_collections
    ]
    
    if missing_collections:
        return ValidationResult(
            is_valid=False,
            message=f"Requirements not met: Missing collections: {', '.join(missing_collections)}",
            code="MISSING_COLLECTIONS",
            details={
                "missing": missing_collections,
                "found": existing_collections
            }
        )
    
    # Phase 2: Validate properties exist on elements
    for collection_name, required_props in property_requirements.items():
        # Skip if collection not in required list (defensive)
        if collection_name not in required_collections:
            continue
        
        # Get the collection
        try:
            collection = next(
                col for col in data.elements 
                if col.name == collection_name
            )
        except StopIteration:
            # Should not happen due to Phase 1 check, but be defensive
            continue
        
        # Check if collection has elements
        if not hasattr(collection, 'elements') or not collection.elements:
            # Empty collection is valid - skip property validation
            continue
        
        # Sample first element to check properties
        sample_element = collection.elements[0]
        
        # Check if element has properties attribute
        if not hasattr(sample_element, 'properties'):
            return ValidationResult(
                is_valid=False,
                message=f"Requirements not met: {collection_name} elements have no 'properties' attribute",
                code="NO_PROPERTIES_ATTRIBUTE",
                details={"collection": collection_name}
            )
        
        # Check if properties is None
        if sample_element.properties is None:
            return ValidationResult(
                is_valid=False,
                message=f"Requirements not met: {collection_name} elements have 'properties' = None",
                code="NULL_PROPERTIES",
                details={"collection": collection_name}
            )
        
        # Check required property keys exist
        missing_props = []
        for prop_key in required_props:
            try:
                # Try to access the property
                _ = sample_element.properties[prop_key]
            except (KeyError, TypeError):
                missing_props.append(prop_key)
        
        if missing_props:
            return ValidationResult(
                is_valid=False,
                message=f"Requirements not met: {collection_name} elements missing properties: {', '.join(missing_props)}",
                code="MISSING_PROPERTIES",
                details={
                    "collection": collection_name,
                    "missing_properties": missing_props,
                    "required_properties": required_props
                }
            )
    
    # All validations passed
    return ValidationResult(
        is_valid=True,
        message="Model structure validation passed",
        code="VALID",
        details={"validated_collections": required_collections}
    )
