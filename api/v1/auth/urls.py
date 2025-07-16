# api/v1/auth/urls.py

from django.urls import path, include
from users.views import get_csrf_token
from users.views import MeView
from .views import DiscordCallbackView
from rest_framework.routers import DefaultRouter
from users.views import UserAdminViewSet

router = DefaultRouter()
router.register(r'admin/users', UserAdminViewSet, basename='admin-users')

urlpatterns = [
    # 🔐 CSRF cookie setter
    path("csrf/", get_csrf_token, name="get_csrf_token"),

    # dj-rest-auth endpoints
    path("", include("dj_rest_auth.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),

    # current-user endpoint
    path("me/", MeView.as_view(), name="custom_me_view"),
    
    path("discord/callback/", DiscordCallbackView.as_view(), name="discord-callback"),
    # Admin-User-API
    path("", include(router.urls)),
]
