# ultrabackend/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    
    path("users/", include("users.urls")),

    # ✅ Versioned API routing
    path("api/v1/", include("api.v1.urls")),

    # ✅ Optional: Allauth routes (needed for Discord OAuth flow)
    path("accounts/discord/", include("allauth.socialaccount.providers.discord.urls")),
    path("accounts/", include("allauth.urls")),
]
