import pytest
from domain.metrics.net_floor_area_ratio import calculate_net_floor_area_ratio
from fixture import make_unit, make_slab

def test_calculate_net_floor_area_ratio_normal():
    slabs = [make_slab(area=100), make_slab(area=200)]
    units = [make_unit(area=50), make_unit(area=100)]
    expected = (50 + 100) / (100 + 200)
    assert calculate_net_floor_area_ratio(units, slabs) == expected

def test_calculate_net_floor_area_ratio_zero_slab():
    slabs = [make_slab(area=0), make_slab(area=0)]
    units = [make_unit(area=50), make_unit(area=100)]
    assert calculate_net_floor_area_ratio(units, slabs) == 0

def test_calculate_net_floor_area_ratio_empty_lists():
    slabs = []
    units = []
    assert calculate_net_floor_area_ratio(units, slabs) == 0
