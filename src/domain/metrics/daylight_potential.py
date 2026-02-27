from domain.model.elements import Facade, Unit
from domain.model.types import MaterialType

def get_window_area(facades: list[Facade]) -> float:
    """
    Calculate total window area from a list of facades.
    """
    return sum(facade.area for facade in facades if facade.material == MaterialType.GLASS)

def calculate_daylight_potential(units: list[Unit], facades: list[Facade]) -> float:
    """
    Calculate daylight potential given a list of units and facades.
    """
    total_window_area = get_window_area(facades)
    total_floor_area = sum(unit.area for unit in units)
    return total_window_area / total_floor_area if total_floor_area > 0 else 0