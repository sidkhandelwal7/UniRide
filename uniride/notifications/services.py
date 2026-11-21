"""
NotificationService: the interface of the Notifications subsystem (Sprint 3).

Only the verification email (US2) is built so far. It is sent right away.
The ride emails (notify, schedule_reminder) and the Notification table come
with the stories that need them.
"""

from django.core.mail import send_mail


def send_verification_email(user, link):
    """Email a new student their one-time verification link (US2)."""
    # Every line is kept under 78 characters. Longer lines make the email get
    # encoded, and then the link is split in two when it is printed in the
    # terminal, so it cannot be copied.
    send_mail(
        subject="Verify your UniRide account",
        message=(
            f"Hi {user.name},\n\n"
            "Open this link to verify your Pitt email and start using UniRide:\n"
            f"{link}\n\n"
            "The link works once and stops working after 1 hour.\n"
            "If it expires, you can ask for a new one on the UniRide website.\n\n"
            "If you did not make a UniRide account, you can ignore this email.\n"
        ),
        from_email=None,  # uses DEFAULT_FROM_EMAIL from settings.py
        recipient_list=[user.email],
    )
