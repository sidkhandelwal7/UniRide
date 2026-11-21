from django import forms

from places import services as place_service

from . import services
from .models import Ride


class PostRideForm(forms.ModelForm):
    """
    US4: post a ride.

    The organizer only has to pick the places and the ride option. The time
    window, open seats, and luggage space have defaults they can change (NFR4).
    """

    # Not required: a blank box means "use the default".
    seats_offered = forms.IntegerField(
        required=False,
        label="Open seats",
        help_text="Leave blank for the most the car holds: 3 for UberX or Lyft Standard, "
        "5 for UberXL or Lyft XL.",
    )
    luggage_space = forms.IntegerField(
        required=False,
        label="Luggage space (bags)",
        help_text="Leave blank for one bag per open seat.",
    )

    class Meta:
        model = Ride
        fields = [
            "meeting_point",
            "destination",
            "ride_option",
            "date",
            "window_start",
            "window_end",
            "seats_offered",
            "luggage_space",
        ]
        labels = {
            "meeting_point": "Meeting point",
            "ride_option": "Ride option",
            "window_start": "Earliest departure time",
            "window_end": "Latest departure time",
        }
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "window_start": forms.TimeInput(attrs={"type": "time"}, format="%H:%M"),
            "window_end": forms.TimeInput(attrs={"type": "time"}, format="%H:%M"),
        }

    def __init__(self, *args, university=None, **kwargs):
        super().__init__(*args, **kwargs)
        # NFR7: students pick from our list of public places, never type an address.
        places = place_service.list_places(university)
        self.fields["meeting_point"].queryset = places
        self.fields["destination"].queryset = places
        self.fields["meeting_point"].empty_label = "Choose a place"
        self.fields["destination"].empty_label = "Choose a place"
        self.fields["ride_option"].empty_label = "Choose UberX, UberXL, Lyft Standard, or Lyft XL"

    def clean(self):
        cleaned = super().clean()
        meeting_point = cleaned.get("meeting_point")
        destination = cleaned.get("destination")
        ride_option = cleaned.get("ride_option")
        date = cleaned.get("date")
        start = cleaned.get("window_start")
        end = cleaned.get("window_end")
        seats = cleaned.get("seats_offered")
        luggage = cleaned.get("luggage_space")

        if meeting_point and destination and meeting_point == destination:
            self.add_error("destination", "The meeting point and destination must be different.")

        if date and start and end:
            if end <= start:
                self.add_error(
                    "window_end", "The latest departure time must be after the earliest one."
                )
            elif services.window_has_passed(date, end):
                self.add_error("window_end", "This time window has already passed.")

        if ride_option:
            most = ride_option.max_open_seats()
            if seats is None:
                seats = most
                cleaned["seats_offered"] = seats
            elif seats < 1:
                self.add_error("seats_offered", "A ride needs at least 1 open seat.")
                seats = None
            elif seats > most:
                self.add_error(
                    "seats_offered",
                    f"A {ride_option.name} has room for at most {most} riders besides you.",
                )
                seats = None

        if luggage is None:
            if seats is not None:
                cleaned["luggage_space"] = seats
        elif luggage < 0:
            self.add_error("luggage_space", "Luggage space cannot be negative.")

        return cleaned
