from django.contrib import messages
from django.shortcuts import redirect, render

from accounts.decorators import verified_required

from . import services
from .forms import PostRideForm


@verified_required
def post_ride(request):
    """US4: post a ride before booking it."""
    if request.method == "POST":
        form = PostRideForm(request.POST, university=request.user.university)
        if form.is_valid():
            services.post_ride(organizer=request.user, **form.cleaned_data)
            messages.success(
                request, "Your ride is posted. Other verified Pitt students can now find it."
            )
            return redirect("home")
    else:
        date, start, end = services.default_window()
        form = PostRideForm(
            university=request.user.university,
            initial={"date": date, "window_start": start, "window_end": end},
        )
    return render(request, "rides/post_ride.html", {"form": form})
