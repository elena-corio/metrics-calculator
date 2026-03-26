from domain.model.types import SectionType
from domain.model.fixture import make_column, make_core, make_slab
from domain.metrics.net_floor_area_ratio import (
    calculate_structural_area,
    calculate_net_floor_area_ratio,
)

def test_calculate_structural_area_circle_and_box():
    columns = [
        make_column(section=SectionType.CIRCLE, size=2.0, thickness=0.2),  # area = pi * 1^2 = pi
        make_column(section=SectionType.BOX, size=2.0, thickness=0.2)      # area = 2^2 = 4
    ]
    cores = [
        make_core(section=SectionType.BOX, size=3.0, thickness=0.3)         # area = 3^2 = 9
    ]
    elements = columns + cores
    area = calculate_structural_area(elements)
    import math
    expected = math.pi + 4 + 9
    assert abs(area - expected) < 1e-6, f"Expected {expected}, got {area}"

def test_calculate_structural_area_empty():
    elements = []
    assert calculate_structural_area(elements) == 0

def test_calculate_net_floor_area_ratio_typical():
    columns = [make_column(section=SectionType.CIRCLE, size=2.0, thickness=0.2)]  # area = pi*1^2
    cores = [make_core(section=SectionType.BOX, size=2.0, thickness=0.2)]         # area = 4
    slabs = [make_slab(area=50), make_slab(area=50)]                              # total = 100
    ratio = calculate_net_floor_area_ratio(columns, cores, slabs)
    import math
    expected_structural = math.pi + 4
    expected_net = 100 - expected_structural
    expected_ratio = expected_net / 100
    assert abs(ratio - expected_ratio) < 1e-6, f"Expected {expected_ratio}, got {ratio}"

def test_calculate_net_floor_area_ratio_zero_gross_area():
    columns = [make_column(section=SectionType.CIRCLE, size=1.0, thickness=0.1)]
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

def test_net_floor_area_ratio_large_columns():
    columns = [make_column(section=SectionType.CIRCLE, size=5.0, thickness=2.5) for _ in range(5)]  # each area = pi*2.5^2
    cores = []
    slabs = [make_slab(area=600)]
    ratio = calculate_net_floor_area_ratio(columns, cores, slabs)
    import math
    col_area = math.pi * 2.5 ** 2
    expected_structural = 5 * col_area
    expected_net = 600 - expected_structural
    expected_ratio = expected_net / 600
    assert abs(ratio - expected_ratio) < 1e-6, f"Expected {expected_ratio}, got {ratio}"
