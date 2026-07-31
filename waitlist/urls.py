from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("v1/api/waitlist/join/", views.join_waitlist, name="join_waitlist"),
]
