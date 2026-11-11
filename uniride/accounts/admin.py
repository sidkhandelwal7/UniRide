from django.contrib import admin

from .models import University, User


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ["name", "email_domain"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "university", "is_verified", "is_staff"]
    # The password hash is left out on purpose so it cannot be edited by hand.
    fields = ["email", "name", "university", "is_verified", "is_active", "is_staff"]
