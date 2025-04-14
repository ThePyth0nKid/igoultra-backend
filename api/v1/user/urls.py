# api/v1/user/urls.py

from django.urls import path
from .views import test_user_view

urlpatterns = [
    path("test/", test_user_view, name="test_user"),
]
