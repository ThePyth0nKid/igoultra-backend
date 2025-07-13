# ultrabackend/urls.py

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

def redirect_to_admin(request):
    """Weiterleitung von der Root-URL zum Django Admin"""
    return redirect('admin:index')

urlpatterns = [
    # Root-URL weiterleiten zum Admin
    path("", redirect_to_admin, name="home"),
    
    # Admin-Interface
    path("admin/", admin.site.urls),

    # Authentication & Social (Discord OAuth + dj-rest-auth)
    path("api/v1/auth/", include("api.v1.auth.urls")),

    # Simple JWT endpoints for obtaining and refreshing JWTs
    path(
        "api/v1/auth/jwt/create/",
        TokenObtainPairView.as_view(),
        name="jwt-create"
    ),
    path(
        "api/v1/auth/jwt/refresh/",
        TokenRefreshView.as_view(),
        name="jwt-refresh"
    ),

    # Allauth routes (optional; needed for Discord OAuth flow)
    path("accounts/", include("allauth.urls")),

    # User-Endpoints
    path("users/", include("users.urls")),

    # Versioned API (inkl. XP, Seasons, etc.)
    path("api/v1/", include("api.v1.urls")),
]

# Nur im DEBUG-Modus: API-Schema und Swagger-UI
if settings.DEBUG:
    from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

    urlpatterns += [
        # OpenAPI-Schema als JSON/YAML
        path(
            "api/schema/",
            SpectacularAPIView.as_view(),
            name="schema"
        ),
        # Swagger-UI zum interaktiven Testen
        path(
            "api/docs/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui"
        ),
    ]
