from domain.model.elements import Facade
from domain.model.types import ProgramType
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
    

def speckle_to_facade(speckle_obj) -> Facade:
    """Convert Speckle object to domain Facade."""
    return Facade(
        cluster_id=speckle_obj.properties["cluster_id"],
        level=speckle_obj.properties["level"],
        material=speckle_obj.properties["material"],
        area=round(speckle_obj.area, 2),
        thickness=0,
        speckle_type=speckle_obj.speckle_type,
        geometry=speckle_obj
    )