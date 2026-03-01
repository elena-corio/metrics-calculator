import pytest
from unittest.mock import MagicMock, patch
from domain.model.elements import ModelElement
from adapters.create_domain_model import map_elements_by_collection, speckle_to_model

class DummyCollection:
    def __init__(self, name, elements):
        self.name = name
        self.elements = elements

class DummyData:
    def __init__(self, collections):
        self.elements = collections

class DummyElement(ModelElement):
    def __init__(self, value):
        self.value = value

def test_map_elements_by_collection_found():
    collection = DummyCollection("TEST", [DummyElement(1), DummyElement(2)])
    data = DummyData([collection])
    result = map_elements_by_collection(data, "TEST", lambda e: e.value * 2)
    assert result == [2, 4]

def test_map_elements_by_collection_not_found():
    data = DummyData([])
    with pytest.raises(ValueError):
        map_elements_by_collection(data, "MISSING", lambda e: e.value * 2)

def test_receive_data_with_magicmock():
    dummy_data = DummyData([
        DummyCollection("COLUMNS", [DummyElement(1)]),
        DummyCollection("CORES", [DummyElement(2)]),
        DummyCollection("FACADES", [DummyElement(3)]),
        DummyCollection("OPEN_SPACES", [DummyElement(4)]),
        DummyCollection("SLABS", [DummyElement(5)]),
        DummyCollection("UNITS", [DummyElement(6)]),
        DummyCollection("VOLUMES", [DummyElement(7)]),
    ])
    with patch("adapters.create_domain_model.operations.receive", return_value=dummy_data) as mock_receive, \
         patch("adapters.create_domain_model.speckle_to_column", side_effect=lambda e: e.value + 1), \
         patch("adapters.create_domain_model.speckle_to_core", side_effect=lambda e: e.value + 2), \
         patch("adapters.create_domain_model.speckle_to_facade", side_effect=lambda e: e.value + 3), \
         patch("adapters.create_domain_model.speckle_to_open_space", side_effect=lambda e: e.value + 4), \
         patch("adapters.create_domain_model.speckle_to_slab", side_effect=lambda e: e.value + 5), \
         patch("adapters.create_domain_model.speckle_to_unit", side_effect=lambda e: e.value + 6), \
         patch("adapters.create_domain_model.speckle_to_volume", side_effect=lambda e: e.value + 7):
        mock_version = MagicMock()
        mock_version.referenced_object = "mock_object_id"
        mock_transport = MagicMock()
        model = speckle_to_model(mock_version, mock_transport)
        mock_receive.assert_called_once_with("mock_object_id", mock_transport)
        assert model.columns == [2]
        assert model.cores == [4]
        assert model.facades == [6]
        assert model.open_spaces == [8]
        assert model.slabs == [10]
        assert model.units == [12]
        assert model.volumes == [14]