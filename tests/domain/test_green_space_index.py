import pytest
from domain.model.fixture import make_unit, make_open_space
from domain.metrics.green_space_distance import (
	get_distance_to_nearest_green,
	calculate_green_space_distance_avg
)

def test_get_distance_to_nearest_green_none():
	unit = make_unit(level=9.0)
	actual = get_distance_to_nearest_green(unit, [])
	assert actual == 1000.0

def test_get_distance_to_nearest_green_some():
	unit = make_unit(level=9.0)
	greens = [make_open_space(level=0.0), make_open_space(level=13.5), make_open_space(level=4.5)]
	# Distances: 9.0-0.0=9.0, 13.5-9.0=4.5, 9.0-4.5=4.5; min=4.5
	actual = get_distance_to_nearest_green(unit, greens)
	expected = 4.5
	assert actual == expected

def test_calculate_green_space_distance_avg():
	units = [make_unit(level=0.0), make_unit(level=4.5), make_unit(level=9.0)]
	greens = [make_open_space(level=4.5)]
	expected = 3.0  # Distances: 4.5, 0.0, 4.5; avg = (4.5+0+4.5)/3 = 3.0
	actual = calculate_green_space_distance_avg(units, greens)
	assert actual == pytest.approx(expected)
