# notifications: Notifications

This folder is the Django app for the **Notifications** subsystem from Sprint 3.

- **Built so far (Sprint 5):** `services.py` has `send_verification_email`, which sends the US2 verification link right away.
- **Class it will own:** Notification (added when the ride emails are built)
- **Interface it provides:** NotificationService (notify, sendVerificationEmail, scheduleReminder)
- **User stories:** US2 (verification email, done), US5, US10, US11, US13, US14, US16, US18
- **Uses:** an email server. Emails print in the terminal unless the `EMAIL_` settings in `.env` are filled in (see `.env.example`).

When you add the Notification model, run `python manage.py makemigrations notifications`.
