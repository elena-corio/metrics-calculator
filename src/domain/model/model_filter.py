from domain.metrics.daylight_potential import get_level_program
from domain.model.types import ProgramType
from domain.model.elements import Model

def filter_model_no_support(model):
    """
    Return a new Model with all elements from levels where the primary program is NOT SUPPORT.
    If all levels are SUPPORT, returns the original model.
    """
    # Find all unique levels
    levels = set(getattr(u, 'level', None) for u in model.units)
    non_support_levels = set()
    for lvl in levels:
        level_model = filter_model(model, lambda e: getattr(e, 'level', None) == lvl)
        if get_level_program(level_model) != ProgramType.SUPPORT:
            non_support_levels.add(lvl)
    # If all levels are SUPPORT, return original model
    if not non_support_levels:
        return model
    # Otherwise, filter elements by non-support levels
    filtered = filter_model(model, lambda e: getattr(e, 'level', None) in non_support_levels)
    # Safety: if filtering removes all units/elements, return original model
    if not filtered.units or all(len(getattr(filtered, attr, [])) == 0 for attr in ['units','slabs','facades','columns','cores','volumes']):
        return model
    return filtered



def filter_model(model, filter_fn):
    return Model(
        columns=[column for column in model.columns if filter_fn(column)],
        cores=[core for core in model.cores if filter_fn(core)],
        facades=[facade for facade in model.facades if filter_fn(facade)],
        open_spaces=model.open_spaces,  # Open spaces are not filtered by cluster_id or level
        slabs=[slab for slab in model.slabs if filter_fn(slab)],
        units=[unit for unit in model.units if filter_fn(unit)],
        volumes=[volume for volume in model.volumes if filter_fn(volume)],
    )