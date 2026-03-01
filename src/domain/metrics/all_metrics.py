from domain.metrics.carbon_efficiency import calculate_carbon_efficiency
from domain.metrics.circulation_efficiency import calculate_circulation_efficiency
from domain.metrics.daylight_potential import calculate_daylight_potential
from domain.metrics.green_space_index import calculate_green_space_index_avg
from domain.metrics.net_floor_area_ratio import calculate_net_floor_area_ratio
from domain.metrics.program_diversity import calculate_program_diversity_index
from domain.metrics.usable_area_ratio import calculate_usable_area_ratio
from domain.metrics.volume_to_envelope import calculate_volume_to_envelope_ratio
from domain.model.elements import Model


def calculate_metrics(model: Model, rulebook: dict) -> dict:
    """
    Calculate metrics for the given model.
    """
    return {
    "daylight_potential": {
      "benchmark": 0.25,
      "value": calculate_daylight_potential(model.units, model.facades, rulebook)
    },
    "green_space_index": {
      "benchmark": 0.80,
      "value": calculate_green_space_index_avg(model.units, model.open_spaces, target=300.0)
    },
    "program_diversity_index": {
      "benchmark": 0.75,
      "value": calculate_program_diversity_index(model.units)
    },
    "circulation_efficiency": {
      "benchmark": 0.75,
      "value": calculate_circulation_efficiency(model.units)
    },
    "usable_area_ratio": {
      "benchmark": 0.70,
      "value": calculate_usable_area_ratio(model.units, rulebook)
    },
    "net_floor_area_ratio": {
      "benchmark": 0.85,
      "value": calculate_net_floor_area_ratio(model.columns, model.cores, model.slabs)
    },
    "volume_to_envelope_ratio": {
      "benchmark": 0.60,
      "value": calculate_volume_to_envelope_ratio(model.volumes, model.facades)
    },
    "carbon_efficiency": {
      "benchmark": 0.50,
      "value": calculate_carbon_efficiency(model.facades, model.slabs, model.columns, model.cores, rulebook, target=600.0)
    }}