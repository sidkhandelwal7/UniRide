"""
AccountService: the interface of the Accounts & Verification subsystem.

The operation names come from our Sprint 3 document (section 3.2). The views
call these functions instead of working with the database directly.
"""

import secrets
from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils import timezone

from notifications import services as notification_service

from .models import University, User

# US2: a verification link stops working after 1 hour.
LINK_LIFETIME = timedelta(hours=1)


def find_university(email):
    """Return the University that matches the part after the @, or None."""
    domain = email.lower().split("@")[-1]
    return University.objects.filter(email_domain=domain).first()


def register(name, email, password):
    """Create a new, unverified account (US1)."""
    return User.objects.create_user(
        email=email,
        name=name,
        password=password,
        university=find_university(email),
    )


def sign_in(request, email, password):
    """Start a session if the email and password match. Returns the user or None (US19)."""
    user = authenticate(request, email=email.lower(), password=password)
    if user is not None:
        login(request, user)
    return user


def sign_out(request):
    """End the session (US19)."""
    logout(request)


def is_verified(user):
    return user.is_verified


def send_verification_link(request, user):
    """
    Make a new one-time code for this user and email them the link (US2).

    The new code replaces the old one, so older links stop working.
    """
    # 16 random bytes (22 characters) is plenty for a code that only works for 1 hour,
    # and it keeps the link short enough to stay on one line in the email.
    user.verification_code = secrets.token_urlsafe(16)
    user.verification_expires_at = timezone.now() + LINK_LIFETIME
    user.save(update_fields=["verification_code", "verification_expires_at"])

    link = request.build_absolute_uri(
        reverse("accounts:verify_email", args=[user.verification_code])
    )
    notification_service.send_verification_email(user, link)


def verify_email(code):
    """
    Check a verification link (US2) and verify the account if the link is good.

    Returns one of:
      "verified"          the link worked and the account is now verified
      "already_verified"  the link was already used
      "expired"           the link is more than 1 hour old
      "invalid"           no account has this code (a typo, or a newer link was sent)
    """
    if not code:
        return "invalid"
    user = User.objects.filter(verification_code=code).first()
    if user is None:
        return "invalid"
    if user.is_verified:
        # We keep the code after it is used so we can say "already used"
        # instead of "this link does not work".
        return "already_verified"
    if timezone.now() > user.verification_expires_at:
        return "expired"

    user.is_verified = True
    user.save(update_fields=["is_verified"])
    return "verified"


def request_verification_link(request, email):
    """
    Send a new link if this email has an account that is not verified yet (US2).

    It does nothing for other emails. The page shows the same message either
    way, so it does not tell anyone which emails have accounts.
    """
    user = User.objects.filter(email=email.lower(), is_verified=False).first()
    if user is not None:
        send_verification_link(request, user)


# The operations below are part of AccountService but are not built yet.


def get_profile(user):
    raise NotImplementedError("US3: not in the MVP")


def update_profile(user, display_name, photo, notification_preferences):
    raise NotImplementedError("US3: not in the MVP")
