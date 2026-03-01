
import math

from domain.model.elements import CurveElement
from domain.model.types import SectionType


def calculate_section_area(element: CurveElement) -> float:
    """
    Calculate cross-sectional area of a curve element.
    """
    if element.section == SectionType.CIRCLE:
        radius = element.size / 2
        return math.pi * radius ** 2 - math.pi * (radius - element.thickness) ** 2
    elif element.section == SectionType.BOX:
        return element.size**2 - (element.size - element.thickness)**2
    else:
        return 0  # Unknown section type