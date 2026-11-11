"""
AccountService: the interface of the Accounts & Verification subsystem.

The operation names come from our Sprint 3 document (section 3.2). The views
call these functions instead of working with the database directly.
"""

from django.contrib.auth import authenticate, login, logout

from .models import University, User


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


# The operations below are part of AccountService but are not built yet.


def verify_email(code):
    raise NotImplementedError("US2: planned for Sprint 5")


def request_verification_link(email):
    raise NotImplementedError("US2: planned for Sprint 5")


def get_profile(user):
    raise NotImplementedError("US3: not in the MVP")


def update_profile(user, display_name, photo, notification_preferences):
    raise NotImplementedError("US3: not in the MVP")
