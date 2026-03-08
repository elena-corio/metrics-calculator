from domain.metrics.carbon_intensity import calculate_carbon_intensity
from domain.metrics.circulation_efficiency import calculate_circulation_efficiency
from domain.metrics.daylight_potential import calculate_daylight_potential
from domain.metrics.green_space_distance import calculate_green_space_distance_avg
from domain.metrics.net_floor_area_ratio import calculate_net_floor_area_ratio
from domain.metrics.program_diversity import calculate_program_diversity_index
from domain.metrics.usable_area_ratio import calculate_usable_area_ratio
from domain.metrics.volume_to_envelope import calculate_volume_to_envelope
from domain.model.elements import Model


def calculate_metrics(model: Model, rulebook: dict) -> dict:
    """
    Calculate metrics for the given model.
    """
    return {
    "gross_floor_area": round(sum(slab.area for slab in model.slabs),2),
    "daylight_potential": round(calculate_daylight_potential(model.units, model.facades, rulebook),2),
    "green_space_distance": round(calculate_green_space_distance_avg(model.units, model.open_spaces, target=250.0),2),
    "program_diversity_index": round(calculate_program_diversity_index(model.units),2),
    "circulation_efficiency": round(calculate_circulation_efficiency(model.units),2),
    "usable_area_ratio": round(calculate_usable_area_ratio(model.units, rulebook),2),
    "net_floor_area_ratio": round(calculate_net_floor_area_ratio(model.columns, model.cores, model.slabs),2),
    "volume_to_envelope": round(calculate_volume_to_envelope(model.facades),2),
    "carbon_intensity": round(calculate_carbon_intensity(model.facades, model.slabs, model.columns, model.cores, rulebook),2)
    }