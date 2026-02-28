import pytest
from fixture import make_unit
from domain.metrics.circulation_efficiency import calculate_circulation_efficiency
from domain.model.types import ProgramType

def test_circulation_efficiency_normal():
    units = [
        make_unit(area=10, program=ProgramType.LIVING),
        make_unit(area=5, program=ProgramType.CIRCULATION),
        make_unit(area=15, program=ProgramType.WORKING)
    ]
    # circulation_area = 5, total_area = 30, efficiency = 1 - (5/30) = 0.833...
    assert calculate_circulation_efficiency(units) == pytest.approx(0.8333, rel=1e-3)

def test_circulation_efficiency_all_circulation():
    units = [
        make_unit(area=10, program=ProgramType.CIRCULATION),
        make_unit(area=5, program=ProgramType.CIRCULATION)
    ]
    # circulation_area = 15, total_area = 15, efficiency = 1 - (15/15) = 0
    assert calculate_circulation_efficiency(units) == 0

def test_circulation_efficiency_no_circulation():
    units = [
        make_unit(area=10, program=ProgramType.LIVING),
        make_unit(area=5, program=ProgramType.WORKING)
    ]
    # circulation_area = 0, total_area = 15, efficiency = 1 - (0/15) = 1
    assert calculate_circulation_efficiency(units) == 1

def test_circulation_efficiency_empty_units():
    units = []
    # total_area = 0, should return 0
    assert calculate_circulation_efficiency(units) == 0