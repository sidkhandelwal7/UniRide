from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from . import services
from .forms import NewLinkForm, RegisterForm, SignInForm


def register(request):
    """US1: create an account. US2: email the verification link right away."""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = services.register(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            services.send_verification_link(request, user)
            messages.success(
                request,
                f"Your account was created. We sent a verification link to {user.email}. "
                "Check your Pitt inbox (and your junk folder). The link works for 1 hour.",
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


def verify_email(request, code):
    """US2: the student opened the link from their verification email."""
    result = services.verify_email(code)
    if result == "verified":
        messages.success(
            request, "Your Pitt email is verified."
        )
        return redirect("home")
    if result == "already_verified":
        messages.success(request, "This link was already used. Your Pitt email is verified.")
        return redirect("home")
    # "expired" or "invalid": the link does not work, so offer a new one.
    return render(
        request,
        "accounts/verify_failed.html",
        {"expired": result == "expired", "form": NewLinkForm()},
    )


def new_link(request):
    """US2: send a new verification link."""
    if request.method == "POST":
        form = NewLinkForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].lower()
            services.request_verification_link(request, email)
            if request.user.is_authenticated and request.user.email == email:
                messages.success(
                    request, f"We sent a new link to {email}. It works for 1 hour."
                )
            else:
                messages.success(
                    request,
                    f"If {email} has an account that is not verified yet, we sent it a new "
                    "link. It works for 1 hour.",
                )
            return redirect("home")
    else:
        initial = {"email": request.user.email} if request.user.is_authenticated else {}
        form = NewLinkForm(initial=initial)
    return render(request, "accounts/new_link.html", {"form": form})


@login_required
def verify_first(request):
    """US2: shown when an unverified student tries to post, find, or join a ride."""
    if request.user.is_verified:
        return redirect("home")
    return render(request, "accounts/verify_first.html")
