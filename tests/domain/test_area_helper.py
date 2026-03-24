from domain.model.types import SectionType
from domain.model.elements import CurveElement
from domain.metrics.area_helper import calculate_section_area

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
