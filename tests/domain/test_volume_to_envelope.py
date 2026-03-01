import pytest
from domain.model.fixture import make_volume, make_facade
from domain.metrics.volume_to_envelope import calculate_volume_to_envelope_ratio

def test_volume_to_envelope_ratio_normal():
    volumes = [make_volume(volume=100), make_volume(volume=50)]
    facades = [make_facade(area=30), make_facade(area=20)]
    # total_volume = 150, envelope_area = 50, ratio = 3.0
    assert calculate_volume_to_envelope_ratio(volumes, facades) == pytest.approx(3.0)

def test_volume_to_envelope_ratio_zero_envelope():
    volumes = [make_volume(volume=100)]
    facades = []
    # envelope_area = 0, should return 0
    assert calculate_volume_to_envelope_ratio(volumes, facades) == 0

def test_volume_to_envelope_ratio_no_volumes():
    volumes = []
    facades = [make_facade(area=30)]
    # total_volume = 0, envelope_area = 30, ratio = 0
    assert calculate_volume_to_envelope_ratio(volumes, facades) == 0