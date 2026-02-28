"""
Calculate volume to envelope ratio given building volumes and facades.
"""

from domain.model.elements import Facade, Volume

def calculate_volume_to_envelope_ratio(volumes: list[Volume], facades: list[Facade]) -> float:
    """
    Calculate volume to envelope ratio given building volumes and facades.
    """
    total_volume = sum(volume.volume for volume in volumes)
    envelope_area = sum(facade.area for facade in facades)
    return total_volume / envelope_area if envelope_area > 0 else 0