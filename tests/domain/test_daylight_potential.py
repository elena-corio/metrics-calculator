import pytest
from domain.metrics.daylight_potential import _is_transparent, get_window_area, calculate_daylight_potential
from domain.model.types import MaterialType
from fixture import load_rulebook, make_facade, make_unit

RULEBOOK = load_rulebook()

def test_is_transparent():
    assert _is_transparent(MaterialType.GLASS, RULEBOOK) == True
    assert _is_transparent(MaterialType.CONCRETE, RULEBOOK) == False

def test_get_window_area_only_glass():
    facades = [
        make_facade(10, MaterialType.GLASS),
        make_facade(20, MaterialType.CONCRETE),
        make_facade(15, MaterialType.GLASS)
    ]
    assert get_window_area(facades, RULEBOOK) == 25

def test_get_window_area_no_glass():
    facades = [
        make_facade(10, MaterialType.CONCRETE),
        make_facade(20, MaterialType.STEEL)
    ]
    assert get_window_area(facades, RULEBOOK) == 0

def test_calculate_daylight_potential_normal():
    facades = [make_facade(area=10, material=MaterialType.GLASS), make_facade(area=5, material=MaterialType.GLASS)]
    units = [make_unit(area=5), make_unit(area=5)]
    # total_window_area = 15, total_floor_area = 10, expected = 1.5
    assert calculate_daylight_potential(units, facades, RULEBOOK) == 1.5

def test_calculate_daylight_potential_zero_floor_area():
    facades = [make_facade(area=10, material=MaterialType.GLASS)]
    units = []
    assert calculate_daylight_potential(units, facades, RULEBOOK) == 0
