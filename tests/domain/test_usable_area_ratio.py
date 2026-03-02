import pytest

from domain.model.fixture import  make_unit
from domain.metrics.usable_area_ratio import _is_usable, calculate_usable_area, calculate_usable_area_ratio
from domain.model.types import ProgramType
from loader import load_rulebook

RULEBOOK = load_rulebook()

def test_is_usable_unit():
    assert _is_usable(ProgramType.LIVING, RULEBOOK) is True
    assert _is_usable(ProgramType.CIRCULATION, RULEBOOK) is False
    assert _is_usable(ProgramType.SUPPORT, RULEBOOK) is False
    
def test_is_usable_missing_program():
    rulebook = load_rulebook()
    # Remove HEALTH from rulebook
    rulebook["program_types"].pop("Health", None)
    assert _is_usable(ProgramType.HEALTH, rulebook) is False
    
def test_get_usable_area():
    units = [
        make_unit(area=10, program=ProgramType.LIVING),
        make_unit(area=5, program=ProgramType.CIRCULATION),
        make_unit(area=15, program=ProgramType.SUPPORT)
    ]
    assert calculate_usable_area(units, RULEBOOK) == 10
    
def test_get_usable_area_no_usable_units():
    units = [
        make_unit(area=10, program=ProgramType.CIRCULATION),
        make_unit(area=5, program=ProgramType.SUPPORT)
    ]
    assert calculate_usable_area(units, RULEBOOK) == 0
    
def test_calculate_usable_area_ratio():
    units = [
        make_unit(area=10, program=ProgramType.LIVING),
        make_unit(area=10, program=ProgramType.WORKING),
        make_unit(area=5, program=ProgramType.CIRCULATION),
        make_unit(area=15, program=ProgramType.SUPPORT)
    ]
    # Usable area = 20, Total area = 40, Ratio = 20/40 = 0.5
    assert calculate_usable_area_ratio(units, RULEBOOK) == pytest.approx(0.5)