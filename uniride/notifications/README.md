# notifications: Notifications (placeholder)

Nothing is built here yet. This folder is the Django app for the **Notifications** subsystem from Sprint 3.

- **Class it will own:** Notification
- **Interface it will provide:** NotificationService (notify, sendVerificationEmail, scheduleReminder)
- **User stories:** US2 (verification email), US5, US10, US11, US13, US14, US16, US18
- **Uses:** an email provider (not chosen yet). For now Django prints emails in the terminal.

When you start working here, add the model to `models.py` and run `python manage.py makemigrations notifications`.
