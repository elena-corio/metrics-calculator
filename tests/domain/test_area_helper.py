from domain.model.types import SectionType
from domain.model.elements import CurveElement
from domain.metrics.area_helper import calculate_section_area, calculate_section_bulk
def test_calculate_section_bulk_circle():
    # For a circle, bulk should be pi * r^2
    element = CurveElement(
        cluster_id='A',
        speckle_type='test_type',
        geometry=None,
        level=0.0,
        material=None,
        length=1.0,
        section=SectionType.CIRCLE,
        size=6.0,  # diameter = 6.0, so radius = 3.0
        thickness=1.0
    )
    bulk = calculate_section_bulk(element)
    import math
    expected_bulk = math.pi * 3.0 ** 2
    assert abs(bulk - expected_bulk) < 1e-6, f"Expected {expected_bulk}, got {bulk}"

def test_calculate_section_bulk_box():
    # For a box, bulk should be size^2
    element = CurveElement(
        cluster_id='B',
        speckle_type='test_type',
        geometry=None,
        level=0.0,
        material=None,
        length=1.0,
        section=SectionType.BOX,
        size=4.0,
        thickness=1.0
    )
    bulk = calculate_section_bulk(element)
    expected_bulk = 16.0
    assert abs(bulk - expected_bulk) < 1e-6, f"Expected {expected_bulk}, got {bulk}"

def test_calculate_section_bulk_unknown():
    # For an unknown section, should return 0
    class DummySection:
        pass
    element = CurveElement(
        cluster_id='C',
        speckle_type='test_type',
        geometry=None,
        level=0.0,
        material=None,
        length=1.0,
        section=None,
        size=5.0,
        thickness=1.0
    )
    bulk = calculate_section_bulk(element)
    assert bulk == 0, f"Expected 0, got {bulk}"

def test_calculate_section_area_circle_large():
    # radius = 2.5, thickness = 2.5, so inner radius = 0
    element = CurveElement(
        cluster_id='A',
        speckle_type='test_type',
        geometry=None,
        level=0.0,
        material=None,
        length=1.0,
        section=SectionType.CIRCLE,
        size=5.0,  # diameter = 5.0, so radius = 2.5
        thickness=2.5
    )
    area = calculate_section_area(element)
    # Should be area of full circle: pi * r^2
    import math
    expected_area = math.pi * 2.5 ** 2
    assert abs(area - expected_area) < 1e-6, f"Expected {expected_area}, got {area}"
