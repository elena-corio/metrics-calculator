from specklepy.api import operations

from adapters.mappers import speckle_to_column, speckle_to_core, speckle_to_facade, speckle_to_open_space, speckle_to_slab, speckle_to_unit, speckle_to_volume
from domain.model.elements import Model, ModelElement

from typing import Callable, TypeVar, List

T = TypeVar('T')

def map_elements_by_collection(
    data: any,  # use actual type
    collection_name: str,
    map_function: Callable[[ModelElement], T]
) -> List[T]:
    """
    Returns a list of mapped elements from the specified collection using the provided map_function.
    Raises ValueError if the collection is not found.
    """
    try:
        elements_collection = next(
            collection for collection in data.elements if collection.name == collection_name
        )
    except StopIteration:
        raise ValueError(f"Collection '{collection_name}' not found in data.elements")
    return [map_function(element) for element in elements_collection.elements]

def receive_and_convert_data(version, transport):
    """
    Receive data from Speckle and convert it to domain model.
    """
    data = operations.receive(version.referenced_object, transport)
    print("Data type: ", type(data))

    mapping = {
        "COLUMNS": speckle_to_column,
        "CORES": speckle_to_core,
        "FACADES": speckle_to_facade,
        "OPEN_SPACES": speckle_to_open_space,
        "SLABS": speckle_to_slab,
        "UNITS": speckle_to_unit,
        "VOLUMES": speckle_to_volume,
    }
    # Creates a dictionary where each key is a lowercase collection name and each value is a list of mapped elements.
    model_kwargs = {
        key.lower(): map_elements_by_collection(data, key, func)
        for key, func in mapping.items()
    }
    # Constructs a Model object, passing each key-value pair as a keyword argument
    return Model(**model_kwargs)