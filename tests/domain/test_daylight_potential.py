from fixture import load_rulebook, make_facade, make_unit
from domain.metrics.daylight_potential import (
    _is_transparent, get_window_area, calculate_daylight_potential
    )
from domain.model.types import MaterialType

RULEBOOK = load_rulebook()

def test_is_transparent():
    assert _is_transparent(MaterialType.GLASS, RULEBOOK) is True
    assert _is_transparent(MaterialType.CONCRETE, RULEBOOK) is False
    
def test_is_transparent_missing_material():
    rulebook = load_rulebook().copy()
    # Remove GLASS from rulebook
    rulebook["material_types"].pop("Glass", None)
    assert _is_transparent(MaterialType.GLASS, rulebook) is False

def test_get_window_area_only_glass():
    facades = [
        make_facade(area=10, material=MaterialType.GLASS),
        make_facade(area=20, material=MaterialType.CONCRETE),
        make_facade(area=15, material=MaterialType.GLASS)
    ]
    assert get_window_area(facades, RULEBOOK) == 25

def test_get_window_area_no_glass():
    facades = [
        make_facade(area=10, material=MaterialType.CONCRETE),
        make_facade(area=20, material=MaterialType.STEEL)
    ]
    assert get_window_area(facades, RULEBOOK) == 0

def test_calculate_daylight_potential_normal():
    facades = [
        make_facade(area=10, material=MaterialType.GLASS), 
        make_facade(area=5, material=MaterialType.GLASS)
    ]
    units = [make_unit(area=5), make_unit(area=5)]
    # total_window_area = 15, total_floor_area = 10, expected = 1.5
    assert calculate_daylight_potential(units, facades, RULEBOOK) == 1.5

def test_calculate_daylight_potential_zero_floor_area():
    facades = [make_facade(area=10, material=MaterialType.GLASS)]
    units = []
    assert calculate_daylight_potential(units, facades, RULEBOOK) == 0
