from domain.model.types import SectionType
from fixture import make_column, make_core, make_slab
from domain.metrics.net_floor_area_ratio import (
    calculate_structural_area,
    calculate_net_floor_area_ratio,
)

def test_calculate_structural_area():
    columns = [
        make_column(section=SectionType.CIRCLE, size=0.5, thickness=0.05),
        make_column(section=SectionType.BOX, size=0.4, thickness=0.04)
    ]
    cores = [
        make_core(section=SectionType.BOX, size=1.0, thickness=0.1)
    ]
    elements = columns + cores
    area = calculate_structural_area(elements)
    assert area > 0

def test_calculate_structural_area_empty():
    elements = []
    assert calculate_structural_area(elements) == 0

def test_calculate_net_floor_area_ratio_normal():
    columns = [make_column(section=SectionType.CIRCLE, size=0.5, thickness=0.05)]
    cores = [make_core(section=SectionType.BOX, size=1.0, thickness=0.1)]
    slabs = [make_slab(area=100), make_slab(area=50)]
    ratio = calculate_net_floor_area_ratio(columns, cores, slabs)
    assert 0 < ratio < 1

def test_calculate_net_floor_area_ratio_zero_gross_area():
    columns = [make_column(section=SectionType.CIRCLE, size=0.5, thickness=0.05)]
    cores = [make_core(section=SectionType.BOX, size=1.0, thickness=0.1)]
    slabs = []
    ratio = calculate_net_floor_area_ratio(columns, cores, slabs)
    assert ratio == 0

def test_calculate_net_floor_area_ratio_no_structural_elements():
    columns = []
    cores = []
    slabs = [make_slab(area=100)]
    ratio = calculate_net_floor_area_ratio(columns, cores, slabs)
    assert ratio == 1
