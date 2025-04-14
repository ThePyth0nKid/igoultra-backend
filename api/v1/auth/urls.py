# api/v1/auth/urls.py

from django.urls import path
from .views import ping

urlpatterns = [
    path("ping/", ping, name="ping"),
]
