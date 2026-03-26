from domain.metrics.carbon_intensity import calculate_carbon_intensity
from domain.metrics.circulation_efficiency import calculate_circulation_efficiency
from domain.metrics.daylight_potential import calculate_daylight_potential
from domain.metrics.green_space_distance import calculate_green_space_distance_avg
from domain.metrics.net_floor_area_ratio import calculate_net_floor_area_ratio
from domain.metrics.program_diversity import calculate_program_diversity_index
from domain.metrics.usable_area_ratio import calculate_usable_area_ratio
from domain.metrics.volume_to_envelope import calculate_volume_to_envelope
from domain.model.elements import Model
from domain.metrics.carbon_intensity import calculate_volume
from collections import defaultdict

def calculate_metrics(model: Model, filtered_model: Model, rulebook: dict) -> dict:
    """
    Calculate metrics for the given model, using rulebook flags to include/exclude SUPPORT levels.
    Pass both the full model and a filtered model (with SUPPORT-only levels removed).
    """
    metrics_rules = rulebook.get("metrics", {})
    def pick_model(metric_name):
        include_support = metrics_rules.get(metric_name, {}).get("include_support", True)
        return model if include_support else filtered_model
    return {
        "gross_floor_area": round(sum(slab.area for slab in pick_model("gross_floor_area").slabs),2),
        "daylight_potential": round(calculate_daylight_potential(pick_model("daylight_potential").units, pick_model("daylight_potential").facades, rulebook),2),
        "green_space_distance": round(calculate_green_space_distance_avg(pick_model("green_space_distance").units, pick_model("green_space_distance").open_spaces),2),
        "program_diversity_index": round(calculate_program_diversity_index(pick_model("program_diversity_index").units),2),
        "circulation_efficiency": round(calculate_circulation_efficiency(pick_model("circulation_efficiency").units),2),
        "usable_area_ratio": round(calculate_usable_area_ratio(pick_model("usable_area_ratio").units, rulebook),2),
        "net_floor_area_ratio": round(calculate_net_floor_area_ratio(pick_model("net_floor_area_ratio").columns, pick_model("net_floor_area_ratio").cores, pick_model("net_floor_area_ratio").slabs),2),
        "volume_to_envelope": round(calculate_volume_to_envelope(pick_model("volume_to_envelope").facades),2),
        "carbon_intensity": round(calculate_carbon_intensity(pick_model("carbon_intensity").facades, pick_model("carbon_intensity").slabs, pick_model("carbon_intensity").columns, pick_model("carbon_intensity").cores, rulebook),2)
    }
    

def calculate_material_breakdown(model: Model) -> dict:
    """
    Returns a dictionary mapping material (lowercase string) to total volume for all elements in the model.
    Only elements with a 'material' attribute are considered.
    """
    material_volumes = defaultdict(float)
    # Gather all elements with a material attribute
    elements = model.facades + model.slabs + model.columns + model.cores
    for element in elements:
        material = getattr(element, 'material', None)
        if material is not None:
            material_name = str(material).lower()
            material_volumes[material_name] += calculate_volume(element)
    return dict(material_volumes)