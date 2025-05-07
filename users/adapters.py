# users/adapters.py

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class DiscordSocialAdapter(DefaultSocialAccountAdapter):
    """
    Adapter to populate and save a new User with Discord data on social login,
    and to allow automatic signup without the intermediate signup form.
    """

    def is_auto_signup_allowed(self, request, sociallogin):
        """
        Return True to automatically create a user account on first social login
        without showing the signup form, even if an email conflict exists.
        """
        return True

    def save_user(self, request, sociallogin, form=None):
        """
        Populate additional fields and save the User instance after
        the social login flow completes.
        """
        user = sociallogin.user
        # Pull Discord ID from the linked SocialAccount
        discord_id = sociallogin.account.uid
        user.discord_id = discord_id

        # Ensure there is a username; fallback to "discord_<id>"
        if not user.username:
            user.username = f"discord_{discord_id}"

        # ultra_name remains blank until the user completes their profile
        # Other fields (email, etc.) are populated by Allauth

        user.save()
        return user
