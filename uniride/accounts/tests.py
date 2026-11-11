from django.test import TestCase
from django.urls import reverse

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
