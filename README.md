# UniRide

- **Team name:** UniRide
- **Course:** CS 1530 Software Engineering, University of Pittsburgh, Fall 2026

## Project purpose

UniRide helps Pitt students find other students traveling to the same destination, such as Pittsburgh International Airport, the Greyhound station, or a concert venue. They can join the same Uber or Lyft and split the fare instead of paying for separate rides. Only students who verify an @pitt.edu email address can post, search for, or join rides.

This semester, we are focusing on the main shared-ride process. An organizer posts a trip before booking it, and other verified students can search for the trip and ask to join. The organizer accepts or declines each request, and the group receives email updates about the ride. When it is time to leave, the organizer books the Uber or Lyft. After the trip, the organizer enters the final fare from the receipt, and UniRide calculates each person's equal share. Payments happen outside UniRide.

## Team

| Member              | Scrum role    | GitHub username |
| ------------------- | ------------- | --------------- |
| Siddhant Khandelwal | Product Owner | sidkhandelwal7  |
|  Terrick Wright     | Scrum Master  |    TLW94-git    |
| Jianghui Chen       | Developer     | EkkoZero        |
| Hayden Gilmer       | Developer     | hmg66           |

## How we plan to build it

We plan to build UniRide as a web app that works in both phone and laptop browsers. We will use Python and the Django web framework. Django provides tools for user accounts, logins, password hashing, form validation, email, and site administration. We plan to use Argon2id for password hashing to meet NFR6.

We will use SQLite while developing the app. The pages will be made with Django templates and basic CSS, so we will not need a separate front-end application. An email service will send verification links and ride updates, while an outside map service will provide the ride map described in FR14. We will organize our work using GitHub issues based on the stories in `user-stories.md`.

## One risk we want to test early

We do not know yet whether UniRide's emails will reliably reach Pitt inboxes. Students must receive a one-time link at their @pitt.edu address to verify their account (FR13), since using Pitt Passport would require university approval (C3). Ride updates must also arrive within 60 seconds (FR12 and NFR2).

If Pitt's spam filters delay or block these messages, students might not be able to finish signing up or could miss important ride updates. We will test this early by sending verification and notification emails to our own Pitt accounts.
