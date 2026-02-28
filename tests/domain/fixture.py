import json
from pathlib import Path

from domain.model.elements import Column, Facade, OpenSpace, Slab, Unit
from domain.model.types import MaterialType, ProgramType, SectionType

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
 
def make_facade(area=50.0, thickness=0.05, material=MaterialType.GLASS):
	return Facade(
		cluster_id="test_cluster",
		speckle_type="test_type",
		geometry=None,
		level=0.0,
		material=material,
		area=area,
		thickness=thickness
	)

def make_slab(area=50.0, thickness=0.2, material=MaterialType.CONCRETE):
	return Slab(
		cluster_id="test_cluster",
		speckle_type="test_type",
		geometry=None,
		level=0.0,
		material=material,
        area=area,
        thickness=thickness
    )
 
def make_column(section=SectionType.CIRCLE,length=3.0, size=0.3, thickness=0.02, material=MaterialType.STEEL):
	return Column(
		cluster_id="test_cluster",
		speckle_type="test_type",
		geometry=None,
		level=0.0,
		material=material,
		length=length,
		section=section,
		size=size,
		thickness=thickness
	)
 
def load_rulebook():
    rulebook_path = Path(__file__).parent / "rulebook.json"
    with open(rulebook_path, encoding="utf-8") as f:
        return json.load(f)

