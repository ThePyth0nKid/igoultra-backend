# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from rankings.constants import REAL_LAYERS, CYBER_LAYERS
from factions.models import Faction
from origins.models import Origin


class User(AbstractUser):
    """
    Custom user model for the iGoUltra platform.
    - Uses Discord for authentication (OAuth2)
    - Username is not necessarily the Discord name
    - Email is optional and not required for login
    - No password is set manually (OAuth-only flows), but kept for superuser creation
    """
    # Discord ID: unique identifier from Discord
    discord_id = models.CharField(
        max_length=64,
        unique=True,
        null=True,
        blank=True,
        help_text=_("Unique ID from the user's Discord account"),
    )

    # In-game display name: chosen by user after initial login
    ultra_name = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        help_text=_("In-game character name chosen by the user"),
    )

    # XP system fields
    xp = models.PositiveIntegerField(
        default=0,
        help_text=_('Total experience points of the user'),
    )
    level = models.PositiveIntegerField(
        default=1,
        help_text=_('Current level based on experience'),
    )
    rank = models.CharField(
        max_length=30,
        default='Unranked',
        help_text=_('Dynamic rank name based on XP and season'),
    )

    # Layer fields for Season-based ranking
    real_layer = models.CharField(
        max_length=20,
        choices=[(l, l) for l in REAL_LAYERS],
        default=REAL_LAYERS[0],
        help_text=_('Current Realitäts-Layer'),
    )
    cyber_layer = models.CharField(
        max_length=20,
        choices=[(l, l) for l in CYBER_LAYERS],
        default=CYBER_LAYERS[0],
        help_text=_('Current Cyber-Layer'),
    )

    # Future avatar URL placeholder
    avatar_url = models.URLField(
        blank=True,
        null=True,
        help_text=_('Optional avatar image or generated artwork URL'),
    )

    # Optional email for communication or recovery
    email = models.EmailField(
        blank=True,
        null=True,
        help_text=_('Optional email address for contact or recovery'),
    )

    # Fraktion (optional, für Onboarding)
    faction = models.ForeignKey(
        Faction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        help_text='Gewählte Fraktion des Users',
    )

    # Herkunft (optional, für Onboarding)
    origin = models.ForeignKey(
        Origin,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        help_text='Herkunft des Users (Ort, Land, Planet, etc.)',
    )

    # Bio (optional, für Onboarding)
    bio = models.TextField(
        blank=True,
        null=True,
        help_text='Individuelle Ultra-Bio des Users',
    )

    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        help_text='Optional: Hochgeladenes Avatar-Bild (PNG/JPG)'
    )

    # No additional required fields; superuser will use username
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'

    def __str__(self):
        """
        String representation: show ultra_name if set, otherwise username.
        """
        return f"{self.ultra_name or self.username}"
