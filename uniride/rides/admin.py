from django.contrib import admin

from .models import Ride, RideOption


@admin.register(RideOption)
class RideOptionAdmin(admin.ModelAdmin):
    list_display = ["name", "provider", "seat_limit", "base_fare", "per_mile_rate"]


@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ["meeting_point", "destination", "date", "window_start", "organizer", "status"]
    list_filter = ["status", "date"]
