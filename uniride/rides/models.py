"""
Ride Management subsystem (Sprint 3).

This app owns the RideOption and Ride classes from our analysis object model.
RideBoard is not a table: its post and search operations are functions in
services.py (post_ride now, search_rides with US7).
"""

from django.conf import settings
from django.db import models


class RideOption(models.Model):
    """An Uber or Lyft ride type that a group can split (US4, US8)."""

    # UberX, UberXL, Lyft Standard, or Lyft XL
    name = models.CharField(max_length=30, unique=True)
    # Uber or Lyft
    provider = models.CharField(max_length=10)
    # How many people the car holds, including the organizer.
    seat_limit = models.PositiveSmallIntegerField()
    # Our own numbers for the fare estimate in US8. They are not Uber or Lyft prices.
    base_fare = models.DecimalField(max_digits=6, decimal_places=2)
    per_mile_rate = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        # Uber first, then Lyft, smaller car first: UberX, UberXL, Lyft Standard, Lyft XL
        ordering = ["-provider", "seat_limit"]

    def __str__(self):
        return self.name

    def max_open_seats(self):
        """Seats the organizer can offer: everyone except the organizer (US4)."""
        return self.seat_limit - 1


class Ride(models.Model):
    """A shared Uber or Lyft ride that an organizer posts before booking it (US4)."""

    OPEN = "open"
    FULL = "full"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    STATUS_CHOICES = [
        (OPEN, "Open"),
        (FULL, "Full"),
        (CANCELLED, "Cancelled"),
        (COMPLETED, "Completed"),
    ]

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="organized_rides"
    )
    meeting_point = models.ForeignKey(
        "places.Location", on_delete=models.PROTECT, related_name="rides_from"
    )
    destination = models.ForeignKey(
        "places.Location", on_delete=models.PROTECT, related_name="rides_to"
    )
    ride_option = models.ForeignKey(RideOption, on_delete=models.PROTECT)
    # The departure window: the group leaves between window_start and window_end on this date.
    date = models.DateField()
    window_start = models.TimeField()
    window_end = models.TimeField()
    seats_offered = models.PositiveSmallIntegerField()
    # Number of bags the ride has room for.
    luggage_space = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=OPEN)
    posted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "window_start"]

    def __str__(self):
        return f"{self.meeting_point} to {self.destination} on {self.date}"
