"""
Calculate daylight potential based on window area and floor area.
"""
import logging
from domain.model.elements import Facade, Unit
from domain.model.types import MaterialType

from domain.model.types import ProgramType

def get_level_program(units: list[Unit]) -> str:
    """
    Determine the primary program for a level, excluding circulation.
    """
    programs = set(unit.program for unit in units)
    non_circulation_programs = [p for p in programs if p != ProgramType.CIRCULATION]
    return non_circulation_programs[0] if non_circulation_programs else ProgramType.CIRCULATION

def get_window_area(facades: list[Facade], units: list[Unit], rulebook: dict) -> float:
    """
    Calculate total window area from a list of facades and units.
    For each facade, determine the program (excluding Circulation) from units,
    look up the glazed ratio for that program in the rulebook, and multiply by facade area.
    This version always applies the program's glazed ratio, regardless of facade material.
    """
    program = get_level_program(units)
    glazed_ratio = rulebook.get("program_types", {}).get(program.value, {}).get("glazed", 0.0)
    # Window area is sum of facade area * glazed ratio (for all facades)
    return sum(facade.area * glazed_ratio for facade in facades)

def calculate_daylight_potential(units: list[Unit], facades: list[Facade], rulebook: dict) -> float:
    """
    Calculate daylight potential given a list of units and facades.
    """
    total_window_area = get_window_area(facades, units, rulebook)
    total_floor_area = sum(unit.area for unit in units)
    return total_window_area / total_floor_area if total_floor_area > 0 else 0
