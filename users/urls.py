# users/urls.py
from django.urls import path
from .views import complete_profile

urlpatterns = [
    path(
        "complete-profile/",
        complete_profile,
        name="complete_profile"   # <-- hier sitzt der Name
    ),
]
