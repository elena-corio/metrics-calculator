"""
Calculate circulation efficiency given a list of units
"""
from domain.model.elements import Unit
from domain.model.types import ProgramType

def calculate_circulation_efficiency(units: list[Unit]) -> float:
    """
    Calculate circulation efficiency
    """
    total_area = sum(unit.area for unit in units)
    circulation_area = sum(unit.area for unit in units if unit.program == ProgramType.CIRCULATION)
    if total_area == 0:
        return 0
    return 1 - (circulation_area / total_area)