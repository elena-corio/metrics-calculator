"""
Calculate green space index based on the distance to the nearest green space.
"""

from domain.model.elements import OpenSpace, Unit

def get_distance_to_nearest_green(res_unit: Unit, green_spaces: list[OpenSpace]) -> float:
    """
    Calculate the vertical distance to the nearest green space.
    """
    if not green_spaces:
        return 1000.0  # A large number to represent no green space available
    
    return min(abs(res_unit.level - green_space.level) for green_space in green_spaces)

def calculate_green_space_distance_avg(res_units: list[Unit], green_spaces: list[OpenSpace]) -> float:
    """
    Calculate avg green space distance for a list of units.
    """
    total_distance = sum(get_distance_to_nearest_green(unit, green_spaces) for unit in res_units)
    return total_distance / len(res_units) if res_units else 0
