# E1: Accounts and verification
Students can make an account, confirm that they go to Pitt, and update their profile.

## US1: Create an account
As a Pitt student, I want to make an account with my name, Pitt email, and a password so that I can use UniRide.
FR: FR1
Priority: Must
MVP: yes

- [ ] The sign-up form asks for a name, email address, and password. It cannot be submitted if any field is empty.
- [ ] An email that does not end in @pitt.edu is rejected, and the student sees a message explaining that only Pitt emails are allowed.
- [ ] If the email already has an account, the student sees a message saying that the account already exists.
- [ ] A new account starts as unverified, and the student is told to check their Pitt inbox for the verification link from US2.
- [ ] The password is stored as a bcrypt or Argon2id hash. The actual password is never stored (NFR6).

## US2: Verify my Pitt email
As a Pitt student, I want to verify my @pitt.edu email so that other students know I actually attend Pitt.
FR: FR13
Priority: Must
MVP: yes

- [ ] UniRide sends a one-time verification link to the student's email right after sign-up.
- [ ] Opening a valid link verifies the account and shows a confirmation message.
- [ ] A link does not work if it was already used or is more than 1 hour old. The student can request a new link.
- [ ] An unverified student cannot post, search for, or join a ride. UniRide asks them to verify their email first.

## US3: Edit my profile
As a Pitt student, I want to update my profile and notification settings so that other riders can recognize me and I only get the emails I want.
FR: FR2
Priority: Should
MVP: no

- [ ] The profile page shows the student's display name, photo, and notification settings.
- [ ] When the student changes their display name or photo, the new version appears on their rides and requests.
- [ ] Profile photos must be JPG or PNG files. Other file types are rejected with a message listing the accepted formats.
- [ ] The student can turn the departure reminder from US16 on or off, and the choice is still there the next time they open their profile.

# E2: Offering a ride
Ride Organizers can post an Uber or Lyft ride, update or cancel it when plans change, and open the ride-hailing app when it is time to book.

## US4: Post a ride
As a Ride Organizer, I want to post a ride quickly before I book it so that students going the same way can join and split the fare.
FR: FR3
Priority: Must
MVP: yes

- [ ] To post a ride, the organizer chooses a meeting point, destination, and ride option: UberX, UberXL, Lyft Standard, or Lyft XL. The other fields have defaults that can be changed before posting (NFR4).
- [ ] The default time window is from now until 30 minutes from now. The organizer can choose a later date and time for a planned trip.
- [ ] Open seats start at 3 for UberX or Lyft Standard and 5 for UberXL or Lyft XL. Luggage space starts at one bag per open seat, but the organizer can lower the seats or change the luggage space.
- [ ] The meeting point and destination come from UniRide's list of public places, such as airports, bus stations, and event venues. Home addresses are not stored (NFR7).
- [ ] The organizer does not enter a fare or book the ride while posting. UniRide estimates the fare in US8, and the organizer books through Uber or Lyft in US6. Driving a personal car is future work under FR20.
- [ ] UniRide shows an error if the meeting point and destination are the same, the time window is invalid, the ride has fewer than 1 seat or more seats than the ride option allows, or the luggage space is negative.
- [ ] A posted ride is saved as "open" and appears in searches that match its meeting point, destination, and date.

## US5: Cancel my ride
As a Ride Organizer, I want to cancel a ride I posted so that everyone who asked to join can make other plans.
FR: FR8, FR12
Priority: Must
MVP: yes

- [ ] Only the organizer can see the Cancel button, and it is only available before the departure time window starts.
- [ ] UniRide asks the organizer to confirm before cancelling the ride.
- [ ] A cancelled ride is marked "cancelled," removed from search results, and closed to new requests.
- [ ] Every rider with a pending or accepted request gets a cancellation email within 60 seconds (FR12 and NFR2).

## US6: Open Uber or Lyft with the trip filled in
As a Ride Organizer, I want to open Uber or Lyft with the trip information already filled in so that I can book the ride faster.
FR: FR16
Priority: Could
MVP: no

- [ ] An "Open in Uber" or "Open in Lyft" button appears on upcoming rides organized by the current user. The button matches the ride option they chose.
- [ ] The button opens the Uber or Lyft app with the meeting point as the pickup and the destination as the drop-off. If the app is missing, it opens the website instead.
- [ ] UniRide does not book the ride. The organizer confirms the booking in Uber or Lyft (C1).

## US18: Change my ride's details
As a Ride Organizer, I want to update a ride after posting it so that I can adjust my plans without cancelling it.
FR: FR3, FR12
Priority: Should
MVP: no

- [ ] Before the departure time window starts, the organizer can change the meeting point, destination, date, time window, ride option, open seats, and luggage space. The same checks from US4 still apply.
- [ ] The organizer cannot lower the open seats below the number of accepted riders or lower the luggage space below the number of bags those riders are bringing.
- [ ] Riders with pending or accepted requests get an email within 60 seconds that lists what changed (FR12 and NFR2).

# E3: Finding and joining a ride
Student Riders can find a ride that works for them, ask to join it, and keep track of their plans.

## US7: Search for rides
As a Student Rider, I want to search by location, date, and time so that I can find a ride that fits my trip.
FR: FR4
Priority: Must
MVP: yes

- [ ] The student chooses the starting location and destination from the same list used when posting a ride.
- [ ] Results only include open rides with matching locations and dates whose departure windows overlap the searched time.
- [ ] Each result shows the departure window, open seats, and estimated share per rider.
- [ ] If nothing matches, the page says that no rides were found.

## US8: View ride details
As a Student Rider, I want to see a ride's details and estimated cost so that I can decide whether to join.
FR: FR5, FR15
Priority: Must
MVP: yes

- [ ] Opening a search result shows the meeting point, destination, date, departure window, open seats, luggage space, and ride option.
- [ ] The page shows the trip distance and an estimated fare. UniRide calculates it from the ride option's base fare, per-mile rate, and distance, rounds it to the nearest dollar, and labels it as an estimate.
- [ ] The organizer's name appears with a "Verified Pitt student" badge.
- [ ] The estimated share is the estimated fare divided by everyone who would be in the ride, including the viewer. For example, an $84 estimate with the organizer and 2 accepted riders shows $21.00 for the viewer.
- [ ] UniRide recalculates the estimated share when another rider is accepted.

## US9: See the ride on a map
As a Student Rider, I want to see the meeting point and destination on a map so that I know where the group is meeting.
FR: FR14
Priority: Should
MVP: no

- [ ] The ride page shows a map from an outside map service with the meeting point and destination marked and named.
- [ ] If the map does not load, the page still shows both location names and says that the map is unavailable.

## US10: Ask to join a ride
As a Student Rider, I want to ask to join a ride and enter how many bags I have so that the organizer can save enough room for me.
FR: FR6, FR12
Priority: Must
MVP: yes

- [ ] A verified student can ask to join an open ride and must enter a bag count of 0 or more.
- [ ] If there is no open seat or not enough luggage space, the request is rejected with a message explaining what is full.
- [ ] A submitted request is saved as "pending," and the rider can see that status on the ride page.
- [ ] A student cannot request the same ride twice or request to join a ride they organized.
- [ ] The organizer gets an email about the request within 60 seconds (FR12 and NFR2).

## US11: Withdraw my request
As a Student Rider, I want to withdraw my request before the ride leaves so that someone else can use the space if my plans change.
FR: FR9, FR12
Priority: Must
MVP: yes

- [ ] A rider can withdraw a pending or accepted request before the departure time window starts.
- [ ] If an accepted rider withdraws, one seat and that rider's luggage space are added back to the ride.
- [ ] The request is marked "withdrawn," and the rider is removed from the estimated share calculation.
- [ ] The organizer gets an email about the withdrawal within 60 seconds (FR12 and NFR2).

## US12: View my rides
As a Student Rider or Ride Organizer, I want to see all of my rides in one place so that I know what is coming up and what is still pending.
FR: FR10
Priority: Should
MVP: yes

- [ ] The My Rides page separates upcoming rides into rides the user organized and rides they asked to join.
- [ ] Each ride shows its date, departure window, destination, and ride status. Join requests also show whether they are pending, accepted, declined, or withdrawn.
- [ ] Completed rides and rides whose departure window has ended move to a Past Rides list.
- [ ] Selecting a ride opens its details page.

# E4: Coordinating the ride
Organizers and riders can decide who is joining, coordinate before pickup, and split the final fare.

## US13: Accept or decline requests
As a Ride Organizer, I want to accept or decline requests so that I can decide who joins my ride.
FR: FR7, FR12
Priority: Must
MVP: yes

- [ ] The organizer can see each pending request with the rider's name, verification badge, and number of bags.
- [ ] Only the ride's organizer can accept or decline its requests.
- [ ] Accepting marks the request "accepted" and adds the rider to the ride. Declining marks it "declined" and does not add the rider.
- [ ] The rider gets an acceptance or decline email within 60 seconds (FR12 and NFR2).

## US14: Enforce my ride's seat and luggage limits
As a Ride Organizer, I want UniRide to track seats and luggage space so that the ride never has more people or bags than it can hold.
FR: FR7, FR12
Priority: Must
MVP: yes

- [ ] Each accepted request removes one open seat and the rider's bag count from the remaining luggage space.
- [ ] When the final seat is taken, the ride becomes "full," leaves the search results, and shows "Full" instead of the join button.
- [ ] Pending requests that no longer fit are automatically declined, and those riders get an email within 60 seconds (FR12 and NFR2).
- [ ] If an accepted rider withdraws and a seat becomes available, the ride becomes "open" and appears in search results again.

## US15: Message my ride group
As a Student Rider or Ride Organizer, I want to message my ride group so that everyone can find each other at the meeting point.
FR: FR11
Priority: Should
MVP: no

- [ ] Only the organizer and accepted riders can open the group chat, read messages, and send messages.
- [ ] Each message shows the sender's name and time, and messages appear in the order they were sent.
- [ ] A rider who withdraws or is declined can no longer open the chat.

## US16: Get a reminder before departure
As a Student Rider or Ride Organizer, I want a reminder before the ride so that I do not miss it.
FR: FR12
Priority: Should
MVP: no

- [ ] Two hours before departure, the organizer and accepted riders get an email with the meeting point, destination, and departure window.
- [ ] UniRide does not send a reminder for a cancelled ride or to a rider whose request was withdrawn or declined.
- [ ] A user who turned reminders off in US3 does not receive the email.

## US17: Split the final fare
As a Ride Organizer, I want to enter the final fare after the trip so that everyone knows their share.
FR: FR15
Priority: Must
MVP: yes

- [ ] The organizer sees a "Ride completed" button after the departure time window starts. The button does not appear before then.
- [ ] Selecting the button asks for the Uber or Lyft receipt total. The value must be more than $0, and saving it marks the ride "completed."
- [ ] UniRide divides the final fare equally between the organizer and accepted riders and shows the amount to the cent. For example, an $84 fare shared by the organizer and 3 riders is $21.00 each.
- [ ] The ride page explains that riders pay the organizer outside UniRide. UniRide does not handle the payment.
