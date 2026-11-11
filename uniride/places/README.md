# places: Places & Maps (placeholder)

Nothing is built here yet. This folder is the Django app for the **Places & Maps** subsystem from Sprint 3.

- **Class it will own:** Location
- **Interface it will provide:** PlaceService (listPlaces, getPlace, distance, mapData, rideHailingLink)
- **User stories:** US4 and US7 (list of places), US8 (distance), US9 (map), US6 (Uber or Lyft link)
- **Uses:** a map service (not chosen yet, US9 is outside the MVP)

When you start working here, add the model to `models.py` and run `python manage.py makemigrations places`.
