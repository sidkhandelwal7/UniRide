# rides: Ride Management

This folder is the Django app for the **Ride Management** subsystem from Sprint 3.

- **Built so far (Sprint 5):** the RideOption and Ride models, the four ride options (migration `0002_add_ride_options`), and the Post a ride page (US4).
- **Classes it owns:** Ride, RideOption. RideBoard is not a table; its post and search operations are functions in `services.py`.
- **Interface it provides:** RideService (postRide, searchRides, getRide, cancelRide, completeRide, ...)
- **User stories:** US4, US5, US7, US8, US12, US17, US18
- **Uses:** PlaceService (places), NotificationService (notifications)

The base fare and per-mile rate of each ride option are our own estimates. They can be changed on the admin site (Rides > Ride options).
