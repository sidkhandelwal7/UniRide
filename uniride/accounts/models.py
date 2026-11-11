"""
Accounts & Verification subsystem (Sprint 3).

This app owns two classes from our analysis object model: University and User.
"""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class University(models.Model):
    """A school whose students can use UniRide. Pitt is the only one for now."""

    name = models.CharField(max_length=100)
    # Example: "pitt.edu". Sign-up only accepts emails that end with this.
    email_domain = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "universities"

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    """Creates users that sign in with an email address instead of a username."""

    def create_user(self, email, name, password, **extra_fields):
        email = self.normalize_email(email).lower()
        user = self.model(email=email, name=name, **extra_fields)
        # set_password stores a hash (Argon2id, see settings.py), never the password.
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password, **extra_fields):
        # Used by "python manage.py createsuperuser" for the admin site.
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        return self.create_user(email, name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    A student account (FR1, FR13).

    AbstractBaseUser adds the password hash and last_login fields.

    Not added yet (planned for Sprint 5):
      - verificationCode, verificationExpiresAt (US2)
      - displayName, photo, notificationPreferences (US3)
    """

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    # New accounts start as unverified (US1). Verifying by email is US2.
    is_verified = models.BooleanField(default=False)
    # Empty only for admin accounts that were made with createsuperuser.
    university = models.ForeignKey(University, on_delete=models.PROTECT, null=True, blank=True)

    # Fields Django needs for sign-in and the admin site.
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email
