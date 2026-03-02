"""
Calculate daylight potential based on window area and floor area.
"""
import logging
from domain.model.elements import Facade, Unit
from domain.model.types import MaterialType

def _is_transparent(material: MaterialType, rulebook: dict) -> bool:
    """
    Check if a material is transparent based on the rulebook.
    """
    material_rule = rulebook["material_types"].get(material.value)
    if material_rule is None:
        logging.warning(f"Material '{material.value}' not found in rulebook.")
        return False
    return material_rule.get("is_transparent", False)

def get_window_area(facades: list[Facade], rulebook: dict) -> float:
    """
    Calculate total window area from a list of facades.
    Uses rulebook.json to check if material is transparent.
    """
    return sum(
        facade.area for facade in facades if _is_transparent(facade.material, rulebook)
    )

def calculate_daylight_potential(units: list[Unit], facades: list[Facade], rulebook: dict) -> float:
    """
    Calculate daylight potential given a list of units and facades.
    """
    total_window_area = get_window_area(facades, rulebook)
    total_floor_area = sum(unit.area for unit in units)
    return total_window_area / total_floor_area if total_floor_area > 0 else 0
