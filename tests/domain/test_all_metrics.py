import pytest
from domain.metrics.all_metrics import calculate_metrics
from domain.model.fixture import make_model, make_unit, make_facade, make_open_space, make_column, make_core, make_slab, make_volume
from loader import load_rulebook

@pytest.fixture
def sample_model():
    units = [make_unit() for _ in range(2)]
    facades = [make_facade() for _ in range(2)]
    open_spaces = [make_open_space() for _ in range(2)]
    columns = [make_column() for _ in range(2)]
    cores = [make_core() for _ in range(2)]
    slabs = [make_slab() for _ in range(2)]
    volumes = [make_volume() for _ in range(2)]
    return make_model(columns, cores, facades, open_spaces, slabs, units, volumes)

RULEBOOK = load_rulebook()

def test_calculate_metrics(sample_model):
    metrics = calculate_metrics(sample_model, RULEBOOK)
    assert isinstance(metrics, dict)
    expected_keys = [
        "daylight_potential",
        "green_space_index",
        "program_diversity_index",
        "circulation_efficiency",
        "usable_area_ratio",
        "net_floor_area_ratio",
        "volume_to_envelope_factor",
        "carbon_efficiency"
    ]
    for key in expected_keys:
        assert key in metrics
        assert "benchmark" in metrics[key]
        assert "value" in metrics[key]
