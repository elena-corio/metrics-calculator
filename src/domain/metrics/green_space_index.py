from domain.model.types import ProgramType
from domain.model.elements import OpenSpace, Unit

def get_distance_to_nearest_green(res_unit: Unit, green_spaces: list[OpenSpace]) -> float:
    """
    Calculate the vertical distance to the nearest green space.
    """
    if not green_spaces:
        return 300.0
    
    return min(abs(res_unit.level - green_space.level) for green_space in green_spaces)


def calculate_green_space_index(res_unit: Unit, green_spaces: list[OpenSpace]) -> float:
    """
    Calculate green space index score for a single unit.
    """
    distance_to_green = get_distance_to_nearest_green(res_unit, green_spaces)
    return max(0, 1 - distance_to_green / 300)


def calculate_green_space_index_avg(res_units: list[Unit], green_spaces: list[OpenSpace]) -> float:
    """
    Calculate avg green space index score for a list of units.
    """
    return sum(calculate_green_space_index(unit, green_spaces) for unit in res_units) / len(res_units)