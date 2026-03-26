from domain.model.fixture import  make_facade, make_unit
from domain.metrics.daylight_potential import get_window_area, calculate_daylight_potential
from domain.model.types import MaterialType, ProgramType
from loader import load_rulebook

RULEBOOK = load_rulebook()

def test_get_window_area_single_program():
    # 2 facades, 1 program (Living, glazed=0.7)
    facades = [
        make_facade(area=10, material=MaterialType.GLASS),
        make_facade(area=20, material=MaterialType.CONCRETE)
    ]
    units = [make_unit(program=ProgramType.LIVING) for _ in range(5)]
    # Only program is Living, glazed ratio = 0.7, window area = (10+20)*0.7 = 21
    assert abs(get_window_area(facades, units, RULEBOOK) - 21) < 1e-6

def test_get_window_area_no_units():
    facades = [make_facade(area=10, material=MaterialType.GLASS)]
    units = []
    assert get_window_area(facades, units, RULEBOOK) == 0
    facades = [make_facade(area=10, material=MaterialType.GLASS)]
    units = [make_unit(program=ProgramType.CIRCULATION) for _ in range(3)] + [make_unit(program=ProgramType.LIVING) for _ in range(2)]
    # Only Living is considered, glazed=0.7, window area = 10*0.7 = 7
    assert abs(get_window_area(facades, units, RULEBOOK) - 7) < 1e-6

    facades = [make_facade(area=10, material=MaterialType.GLASS), make_facade(area=5, material=MaterialType.GLASS)]
    units = [make_unit(area=5, program=ProgramType.LIVING), make_unit(area=5, program=ProgramType.LIVING)]
    # glazed=0.7, window area = (10+5)*0.7=10.5, floor area=10, expected=1.05
    assert abs(calculate_daylight_potential(units, facades, RULEBOOK) - 1.05) < 1e-6

def test_calculate_daylight_potential_zero_floor_area():
    facades = [make_facade(area=10, material=MaterialType.GLASS)]
    units = []
    assert calculate_daylight_potential(units, facades, RULEBOOK) == 0
