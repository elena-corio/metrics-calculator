"""
Fixtures for tests (domain elements, models, etc.)
"""

from domain.model.elements import Column, Core, Facade, Model, OpenSpace, Slab, Unit, Volume
from domain.model.types import MaterialType, ProgramType, SectionType

def make_column(cluster_id="A", level=0.0, section=SectionType.CIRCLE, length=3.0, size=0.3, thickness=0.02, material=MaterialType.STEEL):
	return Column(
		cluster_id=cluster_id,
		speckle_type="test_type",
		geometry=None,
		level=level,
		material=material,
		length=length,
		section=section,
		size=size,
		thickness=thickness
	)
 
def make_core(cluster_id="A", level=0.0, section=SectionType.BOX, length=3.0, size=0.5, thickness=0.05, material=MaterialType.CONCRETE):
	return Core(
		cluster_id=cluster_id,
		speckle_type="test_type",
		geometry=None,
		level=level,
		material=material,
		length=length,
		section=section,
		size=size,
		thickness=thickness
	)

def make_facade(cluster_id="A", level=0.0, area=50.0, thickness=0.05, material=MaterialType.GLASS):
	return Facade(
		cluster_id=cluster_id,
		speckle_type="test_type",
		geometry=None,
		level=level,
		material=material,
		area=area,
		thickness=thickness
	)
 
def make_open_space(cluster_id="A", level=0.0, area=100.0):
	return OpenSpace(
		cluster_id=cluster_id,
		speckle_type="OpenSpace",
		geometry=None,
		level=level,
		area=area
	)
 
def make_slab(cluster_id="A", level=0.0, area=50.0, thickness=0.2, material=MaterialType.CONCRETE):
	return Slab(
		cluster_id=cluster_id,
		speckle_type="test_type",
		geometry=None,
		level=level,
		material=material,
        area=area,
        thickness=thickness
    )
 
def make_unit(cluster_id="A", level=0.0, program=ProgramType.LIVING, area=50.0):
	return Unit(
		cluster_id=cluster_id,
		speckle_type="Unit",
		geometry=None,
		level=level,
		program=program,
		area=area
	)

 
def make_volume(cluster_id="A1", level=0.0, volume=1000.0):
	return Volume(
		cluster_id=cluster_id,
		speckle_type="Volume",
		geometry=None,
		level=level,
		volume=volume
	)
 
def make_model(columns=[], cores=[], facades=[], open_spaces=[], slabs=[], units=[], volumes=[]):
    # Create a Model with only volumes for simplicity
    return Model(
        columns=columns, cores=cores, facades=facades, open_spaces=open_spaces, slabs=slabs, units=units, volumes=volumes
    )


