from django.urls import path

from . import views

app_name = "rides"

urlpatterns = [
    path("post/", views.post_ride, name="post"),
]
