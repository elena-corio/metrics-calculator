"""
Calculate the usable area ratio for a list of units based on the rulebook.
"""
import logging
logging.basicConfig(level=logging.INFO)
from domain.model.types import ProgramType

def _is_usable(program: ProgramType, rulebook: dict) -> bool:
    program_rule = rulebook["program_types"].get(program.value)
    if program_rule is None:
        logging.warning(f"Program '{program.value}' not found in rulebook.")
        return False
    return program_rule.get("is_usable", False)

def calculate_usable_area(units: list, rulebook: dict) -> float:
    """
    Calculate usable area for a list of units.
    """
    return sum(unit.area for unit in units if _is_usable(unit.program, rulebook))
    
def calculate_usable_area_ratio(units: list, rulebook: dict) -> float:
    """
    Calculate usable area ratio for a list of units.
    """
    total_area = sum(unit.area for unit in units)
    logging.info(f"Total area: {total_area}")
    
    usable_area = calculate_usable_area(units, rulebook)
    logging.info(f"Usable area: {usable_area}")
    
    return usable_area / total_area if total_area > 0 else 0