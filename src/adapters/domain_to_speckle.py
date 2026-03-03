import copy
import logging
logging.basicConfig(level=logging.INFO)
from specklepy.api import operations
from specklepy.objects.base import Base
from config import AUTHORS, FUNCTION, SOURCE_MODEL_ID
from domain.metrics.all_metrics import calculate_metrics
from domain.model.elements import Model
from domain.model.model_filter import filter_model

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

def create_element(reference: any, name: str, model: Model, properties: dict, rulebook: dict):
    """
    Create a Speckle element with the geometry from the ModelElement, given name, model, and properties.
    """
    element = copy.deepcopy(reference)
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
        rulebook=rulebook)
    
    cluster_ids = model.cluster_ids()
    logging.info(f"Converting model to Speckle format with clusters: {', '.join(cluster_ids)}")

    for cluster_id in cluster_ids:
        cluster_model = filter_model(model, lambda e: e.cluster_id == cluster_id)
        cluster_base = create_base(
            name=f"Cluster {cluster_id}", 
            model=cluster_model, 
            properties={"cluster_id": cluster_id},
            rulebook=rulebook)

        levels = model.levels_for_cluster(cluster_id)
        logging.info(f"Processing Cluster {cluster_id} with levels: {', '.join(map(str, levels))}")
        
        for level in levels:
            level_model = filter_model(cluster_model, lambda e: e.level == level)
            speckle_obj = next(iter(level_model.volumes), None).geometry  # Volumes represent geometry for the level
            logging.info(f"level_geometry: {speckle_obj}")
            level_geometry = create_element(
                reference=speckle_obj, 
                name=f"Level {level}", 
                model=level_model, 
                properties={"cluster_id": cluster_id, "level": level},
                rulebook=rulebook
            )
            cluster_base.elements.append(level_geometry)

        speckle_model.elements.append(cluster_base)

    return speckle_model

def create_and_send_speckle_model(domain_model: Model, rulebook: dict, transport):
    speckle_model = model_to_speckle(domain_model, rulebook) 
    object_id = operations.send(base=speckle_model, transports=[transport])
    return object_id