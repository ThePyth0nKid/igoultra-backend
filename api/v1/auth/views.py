# api/v1/auth/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.conf import settings
from users.models import User
from rest_framework.authtoken.models import Token

class DiscordCallbackView(APIView):
    permission_classes = []  # public

    def post(self, request):
        code = request.data.get("code")
        if not code:
            return Response({"detail": "Missing code"}, status=status.HTTP_400_BAD_REQUEST)

        # Exchange code for token at Discord
        data = {
            "client_id": settings.DISCORD_CLIENT_ID,
            "client_secret": settings.DISCORD_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.FRONTEND_LOGIN_REDIRECT,
        }
        token_resp = requests.post(
            "https://discord.com/api/oauth2/token",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        if token_resp.status_code != 200:
            return Response({"detail": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)
        access_token = token_resp.json().get("access_token")

        # Fetch user info
        user_resp = requests.get(
            "https://discord.com/api/users/@me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        if user_resp.status_code != 200:
            return Response({"detail": "Failed to fetch Discord user"}, status=status.HTTP_400_BAD_REQUEST)
        discord_data = user_resp.json()

        # Create or get local user
        user, _ = User.objects.get_or_create(
            discord_id=discord_data["id"],
            defaults={
                "username": discord_data["username"],
            }
        )

        # Issue DRF Token
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
