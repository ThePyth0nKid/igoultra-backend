# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for the User model.
    """
    model = User
    list_display = (
        "username",
        "ultra_name",
        "discord_id",
        "xp",
        "level",
        "rank",
        "real_layer",
        "cyber_layer",
        "is_staff",
    )

    fieldsets = UserAdmin.fieldsets + (
        ("Ultra Profile", {
            "fields": (
                "ultra_name",
                "discord_id",
                "xp",
                "level",
                "rank",
                "real_layer",
                "cyber_layer",
                "avatar_url",
            )
        }),
    )
