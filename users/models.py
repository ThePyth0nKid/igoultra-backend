from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# --------------------------------------
# Custom User Model for iGoUltra
# --------------------------------------

class User(AbstractUser):
    """
    Custom user model for the iGoUltra platform.
    - Uses Discord for authentication (OAuth2)
    - Username is not necessarily the Discord name
    - Email is optional and not required for login
    - No password is set manually (OAuth-only)
    """

    # Discord ID (used as unique external identifier)
    discord_id = models.CharField(
        max_length=64,
        unique=True,
        null=True,
        blank=True,
        help_text=_("Unique ID from the user's Discord account"),
    )

    # In-game display name (separate from Discord name)
    ultra_name = models.CharField(
        max_length=50,
        unique=True,
        help_text=_("In-game character name chosen by the user"),
    )

    # XP system
    xp = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    rank = models.CharField(
        max_length=30,
        default="Unranked",
        help_text=_("Dynamic rank name based on XP and season"),
    )

    # Future avatar placeholder (customizable by AI later)
    avatar_url = models.URLField(
        blank=True,
        null=True,
        help_text=_("Optional avatar image or generated artwork"),
    )

    # Optional email (not used for login)
    email = models.EmailField(
        blank=True,
        null=True,
        help_text=_("Optional email for communication or recovery"),
    )

    REQUIRED_FIELDS = ["ultra_name"]
    USERNAME_FIELD = "username"

    def __str__(self):
        return f"{self.ultra_name} ({self.username})"
