from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from . import services
from .forms import RegisterForm, SignInForm


def register(request):
    """US1: create an account."""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            services.register(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            messages.success(
                request,
                "Your account was created. Email verification is not built yet, so you can sign in now.",
            )
            return redirect("accounts:sign_in")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def sign_in(request):
    """US19: sign in with email and password."""
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            user = services.sign_in(
                request,
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                # US19 says to open My Rides here. That page is not built yet,
                # so we go to the home page for now.
                return redirect("home")
            # One message for both cases, so it does not say which one was wrong.
            form.add_error(None, "The email or password is incorrect")
    else:
        form = SignInForm()
    return render(request, "accounts/sign_in.html", {"form": form})


@require_POST
def sign_out(request):
    """US19: sign out."""
    services.sign_out(request)
    messages.success(request, "You are signed out.")
    return redirect("home")
