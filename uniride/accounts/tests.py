from datetime import timedelta

from django.core import mail
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from . import services
from .decorators import verified_required
from .models import User


class RegisterTests(TestCase):
    def test_register_creates_unverified_account(self):
        response = self.client.post(
            reverse("accounts:register"),
            {"name": "Jay Patel", "email": "jay1@pitt.edu", "password": "ride-share-42"},
        )
        self.assertRedirects(response, reverse("accounts:sign_in"))
        user = User.objects.get(email="jay1@pitt.edu")
        self.assertFalse(user.is_verified)
        self.assertEqual(user.university.email_domain, "pitt.edu")

    def test_password_is_stored_as_argon2id_hash(self):
        # NFR6: the password itself is never stored.
        self.client.post(
            reverse("accounts:register"),
            {"name": "Jay Patel", "email": "jay1@pitt.edu", "password": "ride-share-42"},
        )
        user = User.objects.get(email="jay1@pitt.edu")
        self.assertTrue(user.password.startswith("argon2$argon2id$"))
        self.assertNotIn("ride-share-42", user.password)

    def test_non_pitt_email_is_rejected(self):
        response = self.client.post(
            reverse("accounts:register"),
            {"name": "Sam", "email": "sam@gmail.com", "password": "ride-share-42"},
        )
        self.assertContains(response, "Only @pitt.edu email addresses can sign up.")
        self.assertEqual(User.objects.count(), 0)

    def test_email_that_already_has_an_account_is_rejected(self):
        User.objects.create_user(email="jay1@pitt.edu", name="Jay", password="ride-share-42")
        response = self.client.post(
            reverse("accounts:register"),
            {"name": "Jay Again", "email": "JAY1@pitt.edu", "password": "ride-share-42"},
        )
        self.assertContains(response, "An account already exists for this email.")
        self.assertEqual(User.objects.count(), 1)

    def test_empty_fields_are_rejected(self):
        response = self.client.post(
            reverse("accounts:register"), {"name": "", "email": "", "password": ""}
        )
        self.assertContains(response, "This field is required.", count=3)
        self.assertEqual(User.objects.count(), 0)


class SignInAndOutTests(TestCase):
    def setUp(self):
        User.objects.create_user(email="jay1@pitt.edu", name="Jay Patel", password="ride-share-42")

    def test_sign_in_opens_home_page_with_sign_out_button(self):
        response = self.client.post(
            reverse("accounts:sign_in"),
            {"email": "jay1@pitt.edu", "password": "ride-share-42"},
            follow=True,
        )
        self.assertRedirects(response, reverse("home"))
        self.assertContains(response, "Hi, Jay Patel")
        self.assertContains(response, "Sign out")

    def test_wrong_password_shows_one_generic_message(self):
        response = self.client.post(
            reverse("accounts:sign_in"),
            {"email": "jay1@pitt.edu", "password": "wrong-password"},
        )
        self.assertContains(response, "The email or password is incorrect")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_sign_out_ends_the_session(self):
        self.client.login(email="jay1@pitt.edu", password="ride-share-42")
        response = self.client.post(reverse("accounts:sign_out"), follow=True)
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertContains(response, "You are signed out.")


class HomePageTests(TestCase):
    def test_home_page_loads_for_a_visitor(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create account")


class VerifyEmailTests(TestCase):
    """US2: verify my Pitt email."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="jay1@pitt.edu", name="Jay Patel", password="ride-share-42"
        )

    def send_link(self):
        """Send a link the same way sign-up does, and return the link's path."""
        services.send_verification_link(RequestFactory().get("/"), self.user)
        return reverse("accounts:verify_email", args=[self.user.verification_code])

    def test_sign_up_emails_a_one_time_link(self):
        response = self.client.post(
            reverse("accounts:register"),
            {"name": "Maya", "email": "maya1@pitt.edu", "password": "ride-share-42"},
            follow=True,
        )
        maya = User.objects.get(email="maya1@pitt.edu")
        self.assertFalse(maya.is_verified)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["maya1@pitt.edu"])
        self.assertIn(f"/accounts/verify/{maya.verification_code}/", mail.outbox[0].body)
        # US1: the student is told to check their Pitt inbox.
        self.assertContains(response, "Check your Pitt inbox")

    def test_valid_link_verifies_the_account(self):
        path = self.send_link()
        response = self.client.get(path, follow=True)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)
        self.assertContains(response, "Your Pitt email is verified")

    def test_link_does_not_work_a_second_time(self):
        path = self.send_link()
        self.client.get(path)
        response = self.client.get(path, follow=True)
        self.assertContains(response, "This link was already used")

    def test_link_older_than_one_hour_does_not_work(self):
        path = self.send_link()
        self.user.verification_expires_at = timezone.now() - timedelta(minutes=1)
        self.user.save()
        response = self.client.get(path)
        self.assertContains(response, "This link expired")
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_verified)

    def test_new_link_replaces_the_old_one(self):
        old_path = self.send_link()
        self.client.post(reverse("accounts:new_link"), {"email": "jay1@pitt.edu"})
        self.assertEqual(len(mail.outbox), 2)
        response = self.client.get(old_path)
        self.assertContains(response, "This link does not work")

    def test_unverified_student_sees_verify_prompt_instead_of_ride_buttons(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Verify your Pitt email to post, find, and join rides.")
        self.assertNotContains(response, "Post a ride")

    def test_ride_pages_need_a_verified_student(self):
        # The ride pages (US4, US7, US10) use this decorator.
        page = verified_required(lambda request: HttpResponse("ride page"))
        request = RequestFactory().get("/rides/")
        request.user = self.user

        response = page(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("accounts:verify_first"))

        self.user.is_verified = True
        response = page(request)
        self.assertEqual(response.status_code, 200)
        # US19: the browser is told not to keep a copy for the back button.
        self.assertIn("no-store", response["Cache-Control"])
