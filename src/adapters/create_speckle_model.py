from config import AUTHORS, FUNCTION, SOURCE_MODEL_ID
from domain.metrics.all_metrics import calculate_metrics
from domain.model.elements import Model, ModelElement
from domain.model.model_filter import filter_model

from specklepy.objects.base import Base

def create_base(name: str, model: Model, properties: dict, rulebook: dict):
    """
    Create a Speckle Base object with the given name, model, and properties and empty elements list.
    """
    base = Base()
    base.name = name
    base["properties"] = properties
    base["metrics"] = calculate_metrics(model, rulebook)
    base.elements = []
    return base

def create_element(element: ModelElement, name: str, model: Model, properties: dict, rulebook: dict):
    """
    Create a Speckle element with the geometry from the ModelElement, given name, model, and properties.
    """
    element = element.geometry
    element.name = name
    element["properties"] = properties
    element["metrics"] = calculate_metrics(model, rulebook)
    return element

def model_to_speckle(model: Model, rulebook: dict):
    """
    Build hierarchical metrics structure as Speckle Base objects for project, clusters, and levels.
    """
    speckle_model = create_base(
        name = "Hyperbuilding_03", 
        model = model, 
        properties = {
        "authors": AUTHORS, 
        "function": FUNCTION, 
        "source": SOURCE_MODEL_ID}, 
        rulebook = rulebook)

    for cluster_id in model.cluster_ids():
        cluster_model = filter_model(model, lambda e: e.cluster_id == cluster_id)
        cluster_base = create_base(
            name=f"Cluster {cluster_id}", 
            model=cluster_model, 
            properties={"cluster_id": cluster_id},
            rulebook=rulebook)

        for level in model.levels_for_cluster(cluster_id):
            level_model = filter_model(cluster_model, lambda e: e.level == level)
            level_element = next(iter(level_model.volumes), None)  # Volumes represent geometry for the level
            level_geometry = create_element(
                element=level_element, 
                name=f"Level {level}", 
                model=level_model, 
                properties={"cluster_id": cluster_id, "level": level},
                rulebook=rulebook
            )
            cluster_base.elements.append(level_geometry)

        speckle_model.elements.append(cluster_base)

    return speckle_model