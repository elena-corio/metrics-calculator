import pytest
from domain.model.fixture import make_model, make_volume
from adapters.domain_to_speckle import create_base, create_element, model_to_speckle
from specklepy.objects.base import Base 

@pytest.fixture

def sample_model():
    volumes = [
        make_volume(cluster_id="A", level=1, volume=100),
        make_volume(cluster_id="A", level=2, volume=200),
        make_volume(cluster_id="B", level=1, volume=300)
    ]
    # Patch geometry for each volume
    for v in volumes:
        v.geometry = Base()
    return make_model(volumes=volumes)

def test_create_base(sample_model):
    base = create_base("TestBase", sample_model, {"foo": "bar"}, rulebook={})
    assert isinstance(base, Base)
    assert base.name == "TestBase"
    assert base["properties"]["foo"] == "bar"
    assert isinstance(base["metrics"], dict)
    assert base.elements == []

def test_create_element(sample_model):
    # Use first volume as ModelElement
    speckle_obj = sample_model.volumes[0].geometry
    result = create_element(speckle_obj, "TestElement", sample_model, {"baz": 42}, rulebook={})
    assert hasattr(result, "name")
    assert result.name == "TestElement"
    assert result["properties"]["baz"] == 42
    assert isinstance(result["metrics"], dict)

def test_model_to_speckle(sample_model):
    speckle_model = model_to_speckle(sample_model, rulebook={})
    assert isinstance(speckle_model, Base)
    assert hasattr(speckle_model, "elements")
    assert len(speckle_model.elements) == 2  # clusters A and B
    cluster_names = [c.name for c in speckle_model.elements]
    assert "Cluster A" in cluster_names
    assert "Cluster B" in cluster_names
    # Check levels in cluster A
    cluster_a = next(c for c in speckle_model.elements if c.name == "Cluster A")
    level_names = [e.name for e in cluster_a.elements]
    assert set(level_names) == {"Level 1", "Level 2"}
    # Check levels in cluster B
    cluster_b = next(c for c in speckle_model.elements if c.name == "Cluster B")
    level_names_b = [e.name for e in cluster_b.elements]
    assert set(level_names_b) == {"Level 1"}
