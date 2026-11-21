# places: Places & Maps

This folder is the Django app for the **Places & Maps** subsystem from Sprint 3.

- **Built so far (Sprint 5):** the Location model and our first list of eight Pitt places (migration `0002_add_pitt_places`). `services.py` has `list_places`.
- **Class it owns:** Location (name, kind, latitude, longitude, university)
- **Interface it provides:** PlaceService (listPlaces, getPlace, distance, mapData, rideHailingLink)
- **User stories:** US4 and US7 (list of places), US8 (distance), US9 (map), US6 (Uber or Lyft link)
- **Uses:** a map service later (not chosen yet, US9 is outside the MVP)

To add or change a place, use the admin site (Places > Locations). Only add public landmarks or street corners, never a home address (NFR7).
