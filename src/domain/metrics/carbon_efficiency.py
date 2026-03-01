"""
Calculate carbon efficiency of a building based on its elements and materials.
"""
from domain.metrics.area_helper import calculate_section_area
from domain.model.elements import Core, CurveElement, Facade, MeshElement, ModelElement, Slab, Column


def calculate_volume(element: ModelElement) -> float:
    """
    Calculate volume of a building element.
    """
    if isinstance(element, MeshElement):
        return element.area * element.thickness
    elif isinstance(element, CurveElement):
        return element.length * calculate_section_area(element)
    else:
        return 0

def calculate_embodied_carbon(element: ModelElement, rulebook: dict) -> float:
    """
    Calculate embodied carbon of a building element (kgCO2).
    """
    volume = calculate_volume(element)
    material_properties = rulebook["material_types"].get(element.material.value)
    if not material_properties:
        return 0  # Unknown material, assume zero carbon for safety
    weight = volume * material_properties["density"]
    carbon_factor = material_properties["carbon_factor"]
    return weight * carbon_factor
    

def calculate_carbon_efficiency(facades: list[Facade], slabs: list[Slab], columns: list[Column], cores: list[Core], rulebook: dict, target) -> float:
    """
    Calculate carbon efficiency as total embodied carbon per unit area.
    """
    gross_floor_area = sum(slab.area for slab in slabs)
    total_embodied_carbon = sum(calculate_embodied_carbon(element, rulebook) for element in facades + slabs + columns + cores)
    embodied_carbon_intensity = total_embodied_carbon / gross_floor_area if gross_floor_area > 0 else 0
    return max(0, 1 - embodied_carbon_intensity / target)
    
    