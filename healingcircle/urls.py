from django.urls import include, path

urlpatterns = [
    path("", include("waitlist.urls")),
]
