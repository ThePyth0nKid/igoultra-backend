# api/v1/auth/urls.py

from django.urls import path, include
from users.views import get_csrf_token
from users.views import MeView

urlpatterns = [
    # 🔐 CSRF cookie setter
    path("csrf/", get_csrf_token, name="get_csrf_token"),

    # dj-rest-auth endpoints
    path("", include("dj_rest_auth.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),

    # current-user endpoint
    path("me/", MeView.as_view(), name="custom_me_view"),
]
