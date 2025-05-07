from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class DiscordSocialAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.discord_id = data["id"]
        user.username   = f"discord_{data['id']}"
        return user
