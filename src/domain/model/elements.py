from dataclasses import dataclass
from typing import Any
from domain.model.types import MaterialType, ProgramType, SectionType
    
@dataclass
class ModelElement:
    cluster_id: str
    speckle_type: str
    geometry: Any
    level: float
    
@dataclass
class OpenSpace(ModelElement):
    area: float

@dataclass
class Unit (ModelElement):
    program: ProgramType
    area: float

@dataclass
class MeshElement(ModelElement):
    material: MaterialType
    area: float
    thickness: float
    
@dataclass
class CurveElement(ModelElement):
    material: MaterialType
    length: float
    section: SectionType
    size: float
    
@dataclass
class Facade(MeshElement):
    pass
    
@dataclass
class Slabs(MeshElement):
    pass
    
@dataclass
class Core(CurveElement):
    pass

@dataclass
class Column(CurveElement):
    pass

@dataclass
class Model:
    facades: list[Facade]
    #slabs: list[Slabs]
    #cores: list[Core]
    #columns: list[Column]
    units: list[Unit]
    open_spaces: list[OpenSpace]
    levels: list[float]
    clusters: list[str]