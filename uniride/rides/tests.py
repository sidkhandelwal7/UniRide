from datetime import time, timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import University, User
from places.models import Location

from .models import Ride, RideOption


def make_student(email, name, verified=True):
    """A Pitt student account. Verified unless we say otherwise."""
    pitt = University.objects.get(email_domain="pitt.edu")
    return User.objects.create_user(
        email=email, name=name, password="ride-share-42", university=pitt, is_verified=verified
    )


def place(start_of_name):
    """One of the Pitt places added by the places migration."""
    return Location.objects.get(name__startswith=start_of_name)


class PostRideTests(TestCase):
    """US4: post a ride."""

    def setUp(self):
        self.organizer = make_student("dev1@pitt.edu", "Dev Shah")
        self.client.force_login(self.organizer)
        self.tomorrow = timezone.localdate() + timedelta(days=1)

    def post(self, **changes):
        """Post the ride form. Seats and luggage are blank, so they use the defaults."""
        data = {
            "meeting_point": place("Pittsburgh International Airport").pk,
            "destination": place("Cathedral of Learning").pk,
            "ride_option": RideOption.objects.get(name="UberX").pk,
            "date": self.tomorrow.isoformat(),
            "window_start": "18:00",
            "window_end": "18:30",
            "seats_offered": "",
            "luggage_space": "",
        }
        data.update(changes)
        return self.client.post(reverse("rides:post"), data)

    def test_post_page_starts_with_now_to_30_minutes_from_now(self):
        response = self.client.get(reverse("rides:post"))
        form = response.context["form"]
        self.assertEqual(form.initial["date"], timezone.localdate())
        start = form.initial["window_start"]
        end = form.initial["window_end"]
        minutes = (end.hour * 60 + end.minute) - (start.hour * 60 + start.minute)
        # 30 minutes, unless the window was cut off at 11:59 PM.
        self.assertTrue(minutes == 30 or end == time(23, 59))

    def test_ride_is_saved_as_open_with_default_seats_and_luggage(self):
        response = self.post()
        self.assertRedirects(response, reverse("home"))
        ride = Ride.objects.get()
        self.assertEqual(ride.status, Ride.OPEN)
        self.assertEqual(ride.organizer, self.organizer)
        self.assertEqual(ride.seats_offered, 3)
        self.assertEqual(ride.luggage_space, 3)

    def test_xl_starts_with_five_open_seats(self):
        self.post(ride_option=RideOption.objects.get(name="UberXL").pk)
        self.assertEqual(Ride.objects.get().seats_offered, 5)

    def test_same_meeting_point_and_destination_is_rejected(self):
        airport = place("Pittsburgh International Airport").pk
        response = self.post(meeting_point=airport, destination=airport)
        self.assertContains(response, "The meeting point and destination must be different.")
        self.assertFalse(Ride.objects.exists())

    def test_bad_time_window_is_rejected(self):
        response = self.post(window_start="18:30", window_end="18:00")
        self.assertContains(response, "The latest departure time must be after the earliest one.")
        self.assertFalse(Ride.objects.exists())

    def test_too_many_seats_or_negative_luggage_is_rejected(self):
        response = self.post(seats_offered="4", luggage_space="-1")
        self.assertContains(response, "A UberX has room for at most 3 riders besides you.")
        self.assertContains(response, "Luggage space cannot be negative.")
        self.assertFalse(Ride.objects.exists())

    def test_unverified_student_cannot_post(self):
        # US2: unverified students are asked to verify first.
        self.client.force_login(make_student("maya1@pitt.edu", "Maya", verified=False))
        response = self.post()
        self.assertRedirects(response, reverse("accounts:verify_first"))
        self.assertFalse(Ride.objects.exists())
