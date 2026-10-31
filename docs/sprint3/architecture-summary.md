# UniRide Sprint 3 — Architecture summary (Sprint 4 handoff)

Companion to `UniRide_Sprint3_SystemArchitecture.pdf`. This file is the short, machine-readable version of the
decisions that Sprint 4 (tech stack and deployment) builds on. IDs come from Sprint 1 (FR, NFR, C), Sprint 2
(glossary, US1–US18) and Sprint 3 (US19, DG1–DG5).

## Architectural style

Layered (three-tier) architecture inside a client–server system, realized with Django's model–template–view
structure and one centralized relational database. Layers: Presentation → Application logic → Data. A layer
uses only the layer(s) below it. External services (email, map, Uber/Lyft deep link) sit behind adapters.

## Design goals (measurable)

| ID | Goal | Metric | NFR |
|----|------|--------|-----|
| DG1 | Security and privacy (Must) | 100% Argon2id password hashes; 0 home addresses stored (landmark list only); trip locations deleted ≤ 30 days after the ride | NFR6, NFR7 |
| DG2 | Fast ride search | 95% of searches ≤ 2 s with 300 simultaneous users (load test before the final demo) | NFR1 |
| DG3 | Timely notifications | 95% of notifications sent ≤ 60 s after the trigger, measured as `sentAt − triggeredAt` | NFR2 |
| DG4 | Usability and accessibility | ≥ 9/10 first-time testers post a ride ≤ 2 min; 0 WCAG 2.1 AA failures per page | NFR4, NFR5 |
| DG5 | Modifiability | Adding an SMS channel touches only the Notifications subsystem; a second university = configuration only | NFR8, customer input |

## Subsystems → Django apps

| Subsystem | Django app | AOM classes (models) | Provided interface |
|-----------|------------|----------------------|--------------------|
| Web UI | templates + views in each app (no models) | — | HTTP pages |
| Accounts & Verification | `accounts` | User, University | AccountService |
| Ride Management | `rides` | RideBoard, Ride, RideOption | RideService |
| Ride Coordination | `coordination` | RideRequest, Message | CoordinationService |
| Notifications | `notifications` | Notification | NotificationService |
| Places & Maps | `places` | Location | PlaceService |
| Data Storage | Django ORM + database (SQLite dev; production DB chosen in Sprint 4) | persistent form of all nine classes | Persistence |

Dependencies (allowed direction only): Web UI → {AccountService, RideService, CoordinationService, PlaceService};
Ride Coordination → RideService; Ride Management → PlaceService; Accounts, Ride Management, Ride Coordination → NotificationService;
every application subsystem → Persistence; Notifications → Email API (external); Places & Maps → Map API (external).
Notifications depends on no other application subsystem (no cycles).

## Interfaces (analysis-level operation names)

- **AccountService**: register(name, email, password); verifyEmail(code); requestVerificationLink(email); signIn(email, password); signOut(); getProfile(user); updateProfile(user, displayName, photo, notificationPreferences); isVerified(user)
- **RideService**: postRide(organizer, meetingPoint, destination, date, departureWindow, rideOption, seatsOffered, luggageSpace); searchRides(meetingPoint, destination, date, timeWindow); getRide(ride); changeRide(ride, changes); cancelRide(ride); completeRide(ride, finalFare); listRides(user); openSeats(ride); luggageSpaceLeft(ride); estimatedFare(ride); estimatedShare(ride, viewer); finalShare(ride); markFull(ride); markOpen(ride)
- **CoordinationService**: requestToJoin(ride, rider, bags); acceptRequest(request); declineRequest(request); withdrawRequest(request); listRequests(ride); postMessage(ride, sender, text); listMessages(ride, user)
- **NotificationService**: notify(type, ride, recipients); sendVerificationEmail(user, link); scheduleReminder(ride); internal sendPending() run by a scheduler
- **PlaceService**: listPlaces(); getPlace(place); distance(a, b); mapData(a, b); rideHailingLink(rideOption, a, b)
- **Persistence**: save / load / query / delete / transaction for every class (the ORM)

## Revised AOM (nine classes)

University(name, emailDomain) ◆— RideBoard(post, search(meetingPoint, destination, date, timeWindow));
University 1—* User; University 1—* Location (campusLocations);
User(name, email, password, displayName, photo, notificationPreferences, isVerified, verificationCode, verificationExpiresAt; verifyEmail(code), requestVerificationLink());
Ride(date, departureWindow, seatsOffered, luggageSpace, finalFare, status; requestToJoin, openSeats, luggageSpaceLeft, estimatedFare, estimatedShare, changeDetails, complete, finalShare, cancel);
Ride *—1 RideOption(name, provider, seatLimit, baseFare, perMileRate); Ride *—1 meetingPoint Location; Ride *—1 destination Location;
Ride ◆—* RideRequest(bags, status, requestedAt; accept, decline, withdraw) *—1 rider User;
Ride ◆—* Message(text, sentAt) *—1 sender User;
Notification(type, triggeredAt, sentAt) *—1 recipient User, *—1 Ride.

Value sets: Ride.status {open, full, cancelled, completed}; RideRequest.status {pending, accepted, declined, withdrawn};
Location.kind {airport, bus station, event venue, other}; RideOption.name {UberX, UberXL, Lyft Standard, Lyft XL};
Notification.type {request received, request accepted, request declined, ride changed, ride cancelled, reminder}.

Fare rules (FR15): estimatedFare = baseFare + perMileRate × distance(meetingPoint, destination), rounded to the dollar;
estimatedShare = estimatedFare / (organizer + accepted riders + viewer); finalShare = finalFare / (organizer + accepted riders), to the cent.

Future work kept out of the main model: Report (FR17, FR18), User.role/accountStatus (FR18), RideBoard.usageTotals (FR19), driver cost cap (FR20, C2).

## Decisions carried into Sprint 4

- Django; one app per subsystem; templates + views = Web UI; ORM = Data Storage.
- `python -m pip install django[argon2]`; `Argon2PasswordHasher` first in `PASSWORD_HASHERS` (Django's Argon2 hasher uses Argon2id; the framework default is PBKDF2).
- Notifications: outbox table (Notification rows with `triggeredAt`/`sentAt`) emptied by a scheduled sender; email provider chosen after test emails to the team's @pitt.edu inboxes.
- Places: curated `Location` table seeded with Pitt landmarks; map provider chosen in Sprint 4.
- Ride-hailing link (post-MVP, US6): Uber universal link `https://m.uber.com/ul/?action=setPickup&pickup[latitude]=…&pickup[longitude]=…&pickup[nickname]=…&dropoff[latitude]=…&dropoff[longitude]=…&dropoff[nickname]=…` (check whether `client_id` is required); Lyft parameters to confirm.
- Measurements before the final demo: search load test (DG2), outbox timing query (DG3), hallway test + accessibility checker (DG4).

## Backlog

`user-stories.md`: 4 epics, 19 stories (US19 Sign in and out added in Sprint 3, rank 3). Issues created with
`stories_to_github.py` from https://github.com/pitt-se/github-stories (epics as issues, stories as sub-issues).
