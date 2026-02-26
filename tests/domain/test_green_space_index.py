# Import required modules and functions
import pytest
from domain.metrics.green_space_index import (
	get_distance_to_nearest_green,
	calculate_green_space_index,
	calculate_green_space_index_avg
)
from domain.model.elements import OpenSpace, Unit
from domain.model.types import ProgramType


def make_unit(level: float, name=ProgramType.LIVING, area=50.0):
	return Unit(
		cluster_id="c1",
		speckle_type="Unit",
		geometry=None,
		level=level,
		name=name,
		area=area
	)

def make_green(level: float, area=100.0):
	return OpenSpace(
		cluster_id="g1",
		speckle_type="OpenSpace",
		geometry=None,
		level=level,
		area=area
	)

def test_get_distance_to_nearest_green_none():
	unit = make_unit(9.0)
	actual = get_distance_to_nearest_green(unit, [])
	expected = 300.0
	assert actual == expected

def test_get_distance_to_nearest_green_some():
	unit = make_unit(9.0)
	greens = [make_green(0.0), make_green(13.5), make_green(4.5)]
	# Distances: 9.0-0.0=9.0, 13.5-9.0=4.5, 9.0-4.5=4.5; min=4.5
	actual = get_distance_to_nearest_green(unit, greens)
	expected = 4.5
	assert actual == expected

def test_calculate_green_space_index_near():
	unit = make_unit(9.0)
	greens = [make_green(13.5)]
	# distance = abs(9.0 - 13.5) = 4.5
	expected = float(1 - 4.5 / 300)
	actual = calculate_green_space_index(unit, greens)
	assert actual == pytest.approx(expected)

def test_calculate_green_space_index_far():
	unit = make_unit(9.0)
	greens = [make_green(1350.0)]
	# distance = abs(9.0 - 1350.0)  = 1341.0
	expected = float(max(0, 1 - 1341.0 / 300))  # Should be 0
	actual = calculate_green_space_index(unit, greens)
	assert actual == expected

def test_calculate_green_space_index_avg():
	units = [make_unit(0.0), make_unit(4.5), make_unit(9.0)]
	greens = [make_green(4.5)]
	expected_scores = [1 - abs(u.level-4.5)/300 for u in units]
	expected = float(sum(expected_scores) / len(units))
	actual = calculate_green_space_index_avg(units, greens)
	assert actual == pytest.approx(expected)
