"""
Calculate green space index based on the distance to the nearest green space.
"""

from domain.model.elements import OpenSpace, Unit

def get_distance_to_nearest_green(res_unit: Unit, green_spaces: list[OpenSpace], target: float) -> float:
    """
    Calculate the vertical distance to the nearest green space.
    """
    if not green_spaces:
        return target
    
    return min(abs(res_unit.level - green_space.level) for green_space in green_spaces)

def calculate_green_space_index(res_unit: Unit, green_spaces: list[OpenSpace], target) -> float:
    """
    Calculate green space index score for a single unit.
    """
    distance_to_green = get_distance_to_nearest_green(res_unit, green_spaces, target)
    return max(0, 1 - distance_to_green / target)

def calculate_green_space_distance_avg(res_units: list[Unit], green_spaces: list[OpenSpace], target: float) -> float:
    """
    Calculate avg green space distance for a list of units.
    """
    total_distance = sum(get_distance_to_nearest_green(unit, green_spaces, target) for unit in res_units)
    return total_distance / len(res_units) if res_units else 0
