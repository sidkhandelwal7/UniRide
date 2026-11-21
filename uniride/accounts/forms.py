from django import forms
from django.contrib.auth.password_validation import validate_password

from . import services
from .models import User


class RegisterForm(forms.Form):
    """Sign-up form for US1: name, Pitt email, and password."""

    name = forms.CharField(max_length=100)
    email = forms.EmailField(label="Pitt email")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if services.find_university(email) is None:
            raise forms.ValidationError("Only @pitt.edu email addresses can sign up.")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account already exists for this email.")
        return email

    def clean_password(self):
        password = self.cleaned_data["password"]
        # Django's built-in checks, for example at least 8 characters.
        validate_password(password)
        return password


class SignInForm(forms.Form):
    """Sign-in form for US19."""

    email = forms.EmailField(label="Pitt email")
    password = forms.CharField(widget=forms.PasswordInput)
