"""
Calculate net floor area ratio given lists of structural elements.
"""
from domain.metrics.area_helper import calculate_section_area
from domain.model.elements import Column, Core, CurveElement, Slab

def calculate_structural_area(elements: list[CurveElement]) -> float:
    """
    Calculate total area of vertical structural elements (columns and cores).
    """
    return sum(calculate_section_area(element) for element in elements)

def calculate_net_floor_area_ratio(columns: list[Column], cores: list[Core], slabs: list[Slab]) -> float:
    """
    Calculate net floor area ratio given slabs and vertical structural elements.

    """
    gross_floor_area = sum(slab.area for slab in slabs)
    structural_area = calculate_structural_area(columns + cores)
    net_floor_area = gross_floor_area - structural_area
    return net_floor_area / gross_floor_area if gross_floor_area > 0 else 0
