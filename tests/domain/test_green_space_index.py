import pytest
from fixture import load_rulebook, make_unit, make_green
from domain.metrics.green_space_index import (
	get_distance_to_nearest_green,
	calculate_green_space_index,
	calculate_green_space_index_avg
)

RULEBOOK = load_rulebook()

def test_get_distance_to_nearest_green_none():
	unit = make_unit(9.0)
	actual = get_distance_to_nearest_green(unit, [], RULEBOOK)
	target = RULEBOOK["metrics"]["green_space_index"]["target"]
	expected = target
	assert actual == expected

def test_get_distance_to_nearest_green_some():
	unit = make_unit(9.0)
	greens = [make_green(0.0), make_green(13.5), make_green(4.5)]
	# Distances: 9.0-0.0=9.0, 13.5-9.0=4.5, 9.0-4.5=4.5; min=4.5
	actual = get_distance_to_nearest_green(unit, greens, RULEBOOK)
	expected = 4.5
	assert actual == expected

def test_calculate_green_space_index_near():
	unit = make_unit(9.0)
	greens = [make_green(13.5)]
	# distance = abs(9.0 - 13.5) = 4.5
	target = RULEBOOK["metrics"]["green_space_index"]["target"]
	expected = float(1 - 4.5 / target)
	actual = calculate_green_space_index(unit, greens, RULEBOOK)
	assert actual == pytest.approx(expected)

def test_calculate_green_space_index_far():
	unit = make_unit(9.0)
	greens = [make_green(1350.0)]
	# distance = abs(9.0 - 1350.0)  = 1341.0
	target = RULEBOOK["metrics"]["green_space_index"]["target"]
	expected = float(max(0, 1 - 1341.0 / target))  # Should be 0
	actual = calculate_green_space_index(unit, greens, RULEBOOK)
	assert actual == expected

def test_calculate_green_space_index_avg():
	units = [make_unit(0.0), make_unit(4.5), make_unit(9.0)]
	greens = [make_green(4.5)]
	target = RULEBOOK["metrics"]["green_space_index"]["target"]
	expected_scores = [1 - abs(u.level-4.5)/target for u in units]
	expected = float(sum(expected_scores) / len(units))
	actual = calculate_green_space_index_avg(units, greens, RULEBOOK)
	assert actual == pytest.approx(expected)
