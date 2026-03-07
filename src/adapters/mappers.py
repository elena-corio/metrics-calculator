"""
Mappers to convert Speckle objects to domain model elements.
"""

from domain.model.elements import Column, Core, Facade, Slab, Volume
from domain.model.types import MaterialType, ProgramType, SectionType
from domain.model.elements import OpenSpace, Unit


def speckle_to_unit(speckle_obj) -> Unit:
    """Convert Speckle object to domain Unit."""
    return Unit(
        cluster_id=speckle_obj.properties["cluster_id"],
        level=speckle_obj.properties["level"],
        program=ProgramType(speckle_obj.properties["program"].title()),
        area=round(speckle_obj.area, 2),
        speckle_type=speckle_obj.speckle_type,
        geometry=speckle_obj
    )

def speckle_to_open_space(speckle_obj) -> OpenSpace:
    """Convert Speckle object to domain OpenSpace."""
    return OpenSpace(
        cluster_id=speckle_obj.properties["cluster_id"],
        level=speckle_obj.properties["level"],
        area=round(speckle_obj.area, 2),
        speckle_type=speckle_obj.speckle_type,
        geometry=speckle_obj
    )

def speckle_to_volume(speckle_obj) ->Volume:
    """Convert Speckle object to domain Volume."""
    return Volume(
        cluster_id=speckle_obj.properties["cluster_id"],
        level=speckle_obj.properties["level"],
        volume=round(speckle_obj.volume, 2),
        speckle_type=speckle_obj.speckle_type,
        geometry=speckle_obj
    )
    
def speckle_to_facade(speckle_obj) -> Facade:
    """Convert Speckle object to domain Facade."""
    return Facade(
        cluster_id=speckle_obj.properties["cluster_id"],
        level=speckle_obj.properties["level"],
        material=MaterialType(speckle_obj.properties["material"].title()),
        thickness=speckle_obj.properties["thickness"],
        area=round(speckle_obj.area, 2),
        speckle_type=speckle_obj.speckle_type,
        geometry=speckle_obj,
        enclosed_volume=round(speckle_obj.properties["enclosed_volume"], 2)
    )
    
def speckle_to_slab(speckle_obj) -> Slab:
    """Convert Speckle object to domain Slab."""
    return Slab(
        cluster_id=speckle_obj.properties["cluster_id"],
        level=speckle_obj.properties["level"],
        material=MaterialType(speckle_obj.properties["material"].title()),
        thickness=speckle_obj.properties["thickness"],
        area=round(speckle_obj.area, 2),
        speckle_type=speckle_obj.speckle_type,
        geometry=speckle_obj
    )
  
def speckle_to_column(speckle_obj) -> Column:
    """Convert Speckle object to domain Column."""
    return Column(
        cluster_id=speckle_obj.properties["cluster_id"],
        level=speckle_obj.properties["level"],
        material=MaterialType(speckle_obj.properties["material"].title()),
        section=SectionType(speckle_obj.properties["section"].title()),
        size=speckle_obj.properties["size"],
        thickness=speckle_obj.properties["thickness"],
        length=round(speckle_obj.length, 2),
        speckle_type=speckle_obj.speckle_type,
        geometry=speckle_obj
    )
    
def speckle_to_core(speckle_obj) -> Core:
    """Convert Speckle object to domain Core."""
    return Core(
        cluster_id=speckle_obj.properties["cluster_id"],
        level=speckle_obj.properties["level"],
        material=MaterialType(speckle_obj.properties["material"].title()),
        section=SectionType(speckle_obj.properties["section"].title()),
        size=speckle_obj.properties["size"],
        thickness=speckle_obj.properties["thickness"],
        length=round(speckle_obj.length, 2),
        speckle_type=speckle_obj.speckle_type,
        geometry=speckle_obj
    )