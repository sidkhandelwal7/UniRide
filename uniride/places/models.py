"""
Places & Maps subsystem (Sprint 3).

This app owns the Location class from our analysis object model.
"""

from django.db import models


class Location(models.Model):
    """
    A public place where rides meet or go to, like an airport or a venue (US4).

    NFR7: we only store landmarks and street corners from this list, never a
    student's home address.
    """

    AIRPORT = "airport"
    BUS_STATION = "bus station"
    EVENT_VENUE = "event venue"
    OTHER = "other"
    KIND_CHOICES = [
        (AIRPORT, "Airport"),
        (BUS_STATION, "Bus station"),
        (EVENT_VENUE, "Event venue"),
        (OTHER, "Other"),
    ]

    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    # Used to work out the trip distance for the fare estimate (US8),
    # and later for the map (US9).
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    # campusLocations in our object model: each school has its own list (NFR8).
    university = models.ForeignKey(
        "accounts.University", on_delete=models.CASCADE, related_name="campus_locations"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
