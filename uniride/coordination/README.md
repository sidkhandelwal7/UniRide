# coordination: Ride Coordination (placeholder)

Nothing is built here yet. This folder is the Django app for the **Ride Coordination** subsystem from Sprint 3.

- **Classes it will own:** RideRequest, Message
- **Interface it will provide:** CoordinationService (requestToJoin, acceptRequest, declineRequest, withdrawRequest, ...)
- **User stories:** US10, US11, US13, US14, US15
- **Uses:** RideService (rides), NotificationService (notifications)

When you start working here, add the models to `models.py` and run `python manage.py makemigrations coordination`.
