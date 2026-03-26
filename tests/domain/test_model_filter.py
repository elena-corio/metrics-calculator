import pytest
from domain.model.model_filter import filter_model, filter_model_no_support
from domain.model.types import ProgramType
from domain.model.fixture import (
    make_column, make_core, make_facade,  make_slab, make_unit, make_volume, make_model
)

@pytest.fixture
def sample_model():
    columns = [
        make_column(cluster_id="A", level=0.0),
        make_column(cluster_id="B", level=1.0)
    ]
    cores = [
        make_core(cluster_id="A", level=0.0),
        make_core(cluster_id="B", level=1.0)
    ]
    facades = [
        make_facade(cluster_id="A", level=0.0),
        make_facade(cluster_id="B", level=1.0)
    ]
    open_spaces = [
    ]
    slabs = [
        make_slab(cluster_id="A", level=0.0),
        make_slab(cluster_id="B", level=1.0)
    ]
    units = [
        make_unit(cluster_id="A", level=0.0),
        make_unit(cluster_id="B", level=1.0)
    ]
    volumes = [
        make_volume(cluster_id="A", level=0.0),
        make_volume(cluster_id="B", level=1.0)
    ]
    return make_model(columns, cores, facades, open_spaces, slabs, units, volumes)

def test_filter_model_by_cluster_and_level(sample_model):
    # Filter by cluster_id == "A" and level == 0.0
    def filter_fn(e):
        return getattr(e, "cluster_id", None) == "A" and getattr(e, "level", None) == 0.0

    filtered = filter_model(sample_model, filter_fn)

    # All elements should have cluster_id "A" and level 0.0
    for attr in ["columns", "cores", "facades", "slabs", "units", "volumes"]:
        items = getattr(filtered, attr)
        assert len(items) == 1
        assert getattr(items[0], "cluster_id", None) == "A"
        assert getattr(items[0], "level", None) == 0.0

def test_filter_model_no_support():
    # Level 0: SUPPORT, Level 1: LIVING
    units = [
        make_unit(cluster_id="A", level=0.0, program=ProgramType.SUPPORT),
        make_unit(cluster_id="A", level=1.0, program=ProgramType.LIVING)
    ]
    slabs = [
        make_slab(cluster_id="A", level=0.0),
        make_slab(cluster_id="A", level=1.0)
    ]
    model = make_model(slabs=slabs, units=units)
    filtered = filter_model_no_support(model)
    print('Filtered units:', filtered.units)
    print('Filtered slabs:', filtered.slabs)
    print('Filtered model:', filtered)
    # Only level 1.0 should remain
    assert all(u.level == 1.0 for u in filtered.units)
    assert all(s.level == 1.0 for s in filtered.slabs)
    # If all levels are SUPPORT, original model is returned
    units_support = [make_unit(cluster_id="A", level=0.0, program=ProgramType.SUPPORT)]
    slabs_support = [make_slab(cluster_id="A", level=0.0)]
    model_support = make_model(slabs=slabs_support, units=units_support)
    filtered_support = filter_model_no_support(model_support)
    assert filtered_support is model_support
