"""
RideService: the interface of the Ride Management subsystem (Sprint 3).

The operation names come from our Sprint 3 document. Built so far: post_ride (US4).
"""

from datetime import datetime, time, timedelta

from django.utils import timezone

from .models import Ride


def default_window():
    """
    US4: the default departure window is from now until 30 minutes from now.

    Returns (date, start, end). If that would go past midnight, the window
    ends at 11:59 PM so it stays on one day.
    """
    now = timezone.localtime().replace(second=0, microsecond=0)
    end = now + timedelta(minutes=30)
    if end.date() != now.date():
        return now.date(), now.time(), time(23, 59)
    return now.date(), now.time(), end.time()


def window_has_passed(date, window_end):
    """True if the departure window already ended."""
    end = timezone.make_aware(datetime.combine(date, window_end))
    return end < timezone.now()


def post_ride(organizer, meeting_point, destination, ride_option, date,
              window_start, window_end, seats_offered, luggage_space):
    """Save a new open ride (US4). The form checks the values first."""
    return Ride.objects.create(
        organizer=organizer,
        meeting_point=meeting_point,
        destination=destination,
        ride_option=ride_option,
        date=date,
        window_start=window_start,
        window_end=window_end,
        seats_offered=seats_offered,
        luggage_space=luggage_space,
        status=Ride.OPEN,
    )
