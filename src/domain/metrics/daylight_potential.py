from domain.model.elements import Facade, Unit
from domain.model.types import MaterialType
from domain.rules.loader import load_rulebook

def _is_transparent(material: MaterialType, rulebook: dict) -> bool:
    """
    Check if a material is transparent based on the rulebook.
    """
    return rulebook["material_types"].get(material.value, {}).get("is_transparent", False)

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