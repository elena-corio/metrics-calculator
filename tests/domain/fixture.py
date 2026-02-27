from domain.model.elements import Facade, OpenSpace, Slabs, Unit
from domain.model.types import MaterialType, ProgramType

def make_facade(area=50.0, material=MaterialType.GLASS):
	return Facade(
		cluster_id="test_cluster",
		speckle_type="test_type",
		geometry=None,
		level=0.0,
		material=material,
		area=area,
		thickness=0.2
	)

def make_unit(level=0.0, program=ProgramType.LIVING, area=50.0):
	return Unit(
		cluster_id="c1",
		speckle_type="Unit",
		geometry=None,
		level=level,
		program=program,
		area=area
	)

def make_green(level=0.0, area=100.0):
	return OpenSpace(
		cluster_id="g1",
		speckle_type="OpenSpace",
		geometry=None,
		level=level,
		area=area
	)

def make_slab(area=50.0):
    return Slabs(
        cluster_id="test_cluster",
        speckle_type="test_type",
        geometry=None,
        level=0.0,
        material=MaterialType.CONCRETE,
        area=area,
        thickness=0.3
    )
