# users/adapters.py

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount

class DiscordSocialAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter to handle Discord social login without requiring email,
    and to prevent duplicate User instances on repeated logins.
    """

    def pre_social_login(self, request, sociallogin):
        """
        Called just after successful authentication from Discord, but before
        the user is actually logged in. Here, we check if a SocialAccount
        with this Discord uid already exists; if so, we attach the login to
        that existing User instead of creating a new one.
        """
        uid = sociallogin.account.uid
        try:
            existing_account = SocialAccount.objects.get(
                provider=sociallogin.account.provider,
                uid=uid
            )
            # Link this login attempt to the existing user
            sociallogin.account = existing_account
            sociallogin.user = existing_account.user
        except SocialAccount.DoesNotExist:
            # No existing social account, normal signup flow will run
            pass

    def populate_user(self, request, sociallogin, data):
        """
        Prevent Allauth from setting email (we don't require it).
        """
        user = super().populate_user(request, sociallogin, data)
        user.email = ""
        return user

    def save_user(self, request, sociallogin, form=None):
        """
        Create or update the User instance. If this SocialAccount is already
        linked to an existing User (pre_social_login set it), we simply return
        that User without creating a new one.
        """
        # If adapter attached to existing account, skip creation
        if sociallogin.account and sociallogin.account.pk:
            # We still ensure discord_id is set on the User model:
            user = sociallogin.user
            user.discord_id = sociallogin.account.uid
            user.save(update_fields=["discord_id"])
            return user

        # Otherwise, let the superclass create a fresh User
        user = super().save_user(request, sociallogin, form)
        # After creation, set the discord_id and a fallback username
        discord_id = sociallogin.account.uid
        user.discord_id = discord_id
        if not user.username:
            user.username = f"discord_{discord_id}"
        user.save(update_fields=["discord_id", "username"])
        return user
    