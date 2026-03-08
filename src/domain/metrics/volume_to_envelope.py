"""
Calculate volume to envelope ratio given building volumes and facades.
"""

from domain.model.elements import Facade, Volume

def calculate_volume_to_envelope(facades: list[Facade]) -> float:
    """
    Calculate volume to envelope ratio given building volumes and facades.
    """
    total_volume = sum(facade.enclosed_volume for facade in facades)
    envelope_area = sum(facade.area for facade in facades)
    return total_volume / envelope_area if envelope_area > 0 else 0