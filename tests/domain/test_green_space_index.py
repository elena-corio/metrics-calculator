import pytest
from domain.model.fixture import make_unit, make_open_space
from domain.metrics.green_space_distance import (
	get_distance_to_nearest_green,
	calculate_green_space_index,
	calculate_green_space_distance_avg
)

def test_get_distance_to_nearest_green_none():
	unit = make_unit(level=9.0)
	actual = get_distance_to_nearest_green(unit, [], target=300.0)
	assert actual == 300.0

def test_get_distance_to_nearest_green_some():
	unit = make_unit(level=9.0)
	greens = [make_open_space(level=0.0), make_open_space(level=13.5), make_open_space(level=4.5)]
	# Distances: 9.0-0.0=9.0, 13.5-9.0=4.5, 9.0-4.5=4.5; min=4.5
	actual = get_distance_to_nearest_green(unit, greens, target=300.0)
	expected = 4.5
	assert actual == expected

def test_calculate_green_space_index_near():
	unit = make_unit(level=9.0)
	greens = [make_open_space(level=13.5)]
	# distance = abs(9.0 - 13.5) = 4.5
	target = 300.0
	expected = float(1 - 4.5 / target)
	actual = calculate_green_space_index(unit, greens, target)
	assert actual == pytest.approx(expected)

def test_calculate_green_space_index_far():
	unit = make_unit(level=9.0)
	greens = [make_open_space(level=1350.0)]
	# distance = abs(9.0 - 1350.0)  = 1341.0
	target = 300.0
	expected = float(max(0, 1 - 1341.0 / target))  # Should be 0
	actual = calculate_green_space_index(unit, greens, target)
	assert actual == expected

def test_calculate_green_space_index_avg():
	units = [make_unit(level=0.0), make_unit(level=4.5), make_unit(level=9.0)]
	greens = [make_open_space(level=4.5)]
	target = 300.0
	expected_scores = [1 - abs(u.level-4.5)/target for u in units]
	expected = float(sum(expected_scores) / len(units))
	actual = calculate_green_space_distance_avg(units, greens, target)
	assert actual == pytest.approx(expected)
