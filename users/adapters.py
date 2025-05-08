from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_username

class DiscordSocialAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter to handle Discord social login without requiring email.
    It overrides default Allauth behavior to support:
    - auto signup
    - no email
    - generated username fallback
    - storing Discord ID
    """

    def is_auto_signup_allowed(self, request, sociallogin):
        """
        Allow automatic user creation without redirecting to a signup form.
        """
        return True

    def populate_user(self, request, sociallogin, data):
        """
        Prevent Allauth from injecting 'email' into the user model.
        """
        user = super().populate_user(request, sociallogin, data)
        user.email = ""  # Ensure email is empty (not required)
        return user

    def save_user(self, request, sociallogin, form=None):
        """
        Set fields like username and Discord ID after login completes.
        """
        user = sociallogin.user
        discord_id = sociallogin.account.uid
        user.discord_id = discord_id

        # Fallback username if none exists
        if not user.username:
            user.username = f"discord_{discord_id}"

        # Leave ultra_name empty for frontend onboarding step
        user.save()
        return user
