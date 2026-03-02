import pytest
from domain.model.fixture import make_volume, make_facade
from domain.metrics.volume_to_envelope import calculate_volume_to_envelope_factor

def test_volume_to_envelope_factor_normal():
    volumes = [make_volume(volume=100), make_volume(volume=50)]
    facades = [make_facade(area=30), make_facade(area=20)]
    # total_volume = 150, envelope_area = 50, factor = 150 / (50 * 10) = 0.3
    assert calculate_volume_to_envelope_factor(volumes, facades) == pytest.approx(0.3)

def test_volume_to_envelope_factor_zero_envelope():
    volumes = [make_volume(volume=100)]
    facades = []
    # envelope_area = 0, should return 0
    assert calculate_volume_to_envelope_factor(volumes, facades) == 0

def test_volume_to_envelope_factor_no_volumes():
    volumes = []
    facades = [make_facade(area=30)]
    # total_volume = 0, envelope_area = 30, factor = 0
    assert calculate_volume_to_envelope_factor(volumes, facades) == 0