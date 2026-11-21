"""
PlaceService: the interface of the Places & Maps subsystem (Sprint 3).

Built so far: list_places (US4, US7). distance, mapData, and rideHailingLink
come with US8, US9, and US6.
"""

from .models import Location


def list_places(university):
    """The places students at this school can pick as a meeting point or destination."""
    return Location.objects.filter(university=university)
