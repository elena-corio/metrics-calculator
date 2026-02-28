"""
Calculate net floor area ratio for a list of units and slabs.
"""

from domain.model.elements import Slab, Unit

# Note: it can also be calculated as slab area - core area - column area
# so it only depedns on structural model
def calculate_net_floor_area_ratio(units: list[Unit], slabs: list[Slab]) -> float:
    """
    Calculate net floor area ratio for a list of units.

    """
    net_floor_area = sum(unit.area for unit in units)
    gross_floor_area = sum(slab.area for slab in slabs)
    return net_floor_area / gross_floor_area if gross_floor_area > 0 else 0
