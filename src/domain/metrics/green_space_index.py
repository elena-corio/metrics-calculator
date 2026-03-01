"""
Calculate green space index based on the distance to the nearest green space.
"""

from domain.model.elements import OpenSpace, Unit

def get_distance_to_nearest_green(res_unit: Unit, green_spaces: list[OpenSpace], rulebook: dict) -> float:
    """
    Calculate the vertical distance to the nearest green space.
    """
    if not green_spaces:
        return rulebook["metrics"]["green_space_index"]["target"]
    
    return min(abs(res_unit.level - green_space.level) for green_space in green_spaces)


def calculate_green_space_index(res_unit: Unit, green_spaces: list[OpenSpace], rulebook: dict) -> float:
    """
    Calculate green space index score for a single unit.
    """
    distance_to_green = get_distance_to_nearest_green(res_unit, green_spaces, rulebook)
    target = rulebook["metrics"]["green_space_index"]["target"]
    return max(0, 1 - distance_to_green / target)

def calculate_green_space_index_avg(res_units: list[Unit], green_spaces: list[OpenSpace], rulebook: dict) -> float:
    """
    Calculate avg green space index score for a list of units.
    """
    total_score = sum(calculate_green_space_index(unit, green_spaces, rulebook) for unit in res_units)
    return total_score / len(res_units) if res_units else 0
