import pytest

from domain.model.types import MaterialType, SectionType
from fixture import load_rulebook, make_facade, make_slab, make_column
from domain.metrics.carbon_efficiency import (
    calculate_cross_section_area,
    calculate_volume,
    calculate_embodied_carbon,
    calculate_carbon_efficiency,
)

RULEBOOK = load_rulebook()

def test_calculate_cross_section_area_circular():
    curve = make_column(section=SectionType.CIRCLE, size=0.5, thickness=0.05)
    area = calculate_cross_section_area(curve)
    assert area > 0

def test_calculate_cross_section_area_box():
    curve = make_column(section=SectionType.BOX, size=0.5, thickness=0.05)
    area = calculate_cross_section_area(curve)
    assert area > 0

def test_calculate_cross_section_area_invalid_section():
    class FakeSection:
        value = "TRIANGLE"
    curve = make_column(section=FakeSection, size=0.5, thickness=0.05)
    area = calculate_cross_section_area(curve)
    assert area == 0  # Function returns 0 for unknown section

def test_calculate_volume_mesh_element():
    mesh = make_slab(area=10, thickness=0.2)
    volume = calculate_volume(mesh)
    assert volume == pytest.approx(2.0)

def test_calculate_volume_curve_element():
    curve = make_column(section=SectionType.CIRCLE, size=0.5, thickness=0.05, length=3)
    volume = calculate_volume(curve)
    assert volume > 0

def test_calculate_volume_other_element():
    class DummyElement:
        pass
    dummy = DummyElement()
    volume = calculate_volume(dummy)
    assert volume == 0

def test_calculate_embodied_carbon_valid():
    slab = make_slab(area=10, thickness=0.2, material=MaterialType.CONCRETE)
    carbon = calculate_embodied_carbon(slab, RULEBOOK)
    assert carbon > 0

def test_calculate_embodied_carbon_missing_material():
    RULEBOOK["material_types"].pop("Concrete", None)
    slab = make_slab(area=10, thickness=0.2, material=MaterialType.CONCRETE)
    assert calculate_embodied_carbon(slab, RULEBOOK) == 0  # Should return 0 for unknown material

def test_calculate_carbon_efficiency_normal():
    facades = [make_facade(area=20, thickness=0.1, material=MaterialType.GLASS)]
    slabs = [make_slab(area=100, thickness=0.2, material=MaterialType.CONCRETE)]
    columns = [make_column(length=3, size=0.3, thickness=0.03, section=SectionType.CIRCLE, material=MaterialType.STEEL)]
    efficiency = calculate_carbon_efficiency(facades, slabs, columns, RULEBOOK)
    assert 0 <= efficiency <= 1

def test_calculate_carbon_efficiency_zero_gross_area():
    facades = [make_facade(area=20, thickness=0.1, material=MaterialType.GLASS)]
    slabs = []
    columns = [make_column(length=3, size=0.3, thickness=0.03, section=SectionType.CIRCLE, material=MaterialType.STEEL)]
    efficiency = calculate_carbon_efficiency(facades, slabs, columns, RULEBOOK)
    assert efficiency == 1  # embodied_carbon_intensity is 0

def test_calculate_carbon_efficiency_high_embodied_carbon():
    slabs = [make_slab(area=100, thickness=0.2, material=MaterialType.CONCRETE)]
    # artificially high carbon factor in rulebook
    rulebook = load_rulebook()
    rulebook["material_types"]["Concrete"]["carbon_factor"] = 1000
    facades = []
    columns = []
    efficiency = calculate_carbon_efficiency(facades, slabs, columns, rulebook)
    assert efficiency == 0  # efficiency clamped to minimum 0