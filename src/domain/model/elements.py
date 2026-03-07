"""
Domain model elements representing the building components and spaces.
"""
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
class Volume(ModelElement):
    volume: float
    
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
    thickness: float
    
@dataclass
class Facade(MeshElement):
    enclosed_volume: float
    pass
    
@dataclass
class Slab(MeshElement):
    pass
    
@dataclass
class Core(CurveElement):
    pass

@dataclass
class Column(CurveElement):
    pass

@dataclass
class Model:
    columns: list[Column]
    cores: list[Core]
    facades: list[Facade]
    open_spaces: list[OpenSpace]
    slabs: list[Slab]
    units: list[Unit]
    volumes: list[Volume]
    
    def cluster_ids(self):
        return sorted(set(v.cluster_id for v in self.volumes))

    def levels_for_cluster(self, cluster_id):
        return sorted(set(v.level for v in self.volumes if v.cluster_id == cluster_id))
