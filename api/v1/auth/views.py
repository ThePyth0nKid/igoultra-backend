# api/v1/auth/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.conf import settings
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
import traceback

class DiscordCallbackView(APIView):
    permission_classes = []  # public endpoint

    def post(self, request):
        try:
            code = request.data.get("code")
            redirect_uri = request.data.get("redirect_uri") or settings.FRONTEND_LOGIN_REDIRECT

            # Debug: Log the incoming payload
            print("🔵 DiscordCallbackView payload:", {"code": code, "redirect_uri": redirect_uri})

            if not code:
                return Response({"detail": "Missing code"}, status=status.HTTP_400_BAD_REQUEST)

            # 1) Exchange code for Discord access token
            data = {
                "client_id": settings.DISCORD_CLIENT_ID,
                "client_secret": settings.DISCORD_CLIENT_SECRET,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
            }
            print("🔵 Token exchange request to Discord:", data)

            token_resp = requests.post(
                "https://discord.com/api/oauth2/token",
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )

            # Debug: Log Discord's raw response
            print("🔴 Discord token response status:", token_resp.status_code)
            print("🔴 Discord token response body:", token_resp.text)

            if token_resp.status_code != 200:
                return Response(
                    {"detail": "Invalid code or redirect URI", "discord_error": token_resp.text},
                    status=status.HTTP_400_BAD_REQUEST
                )

            discord_access = token_resp.json().get("access_token")

            # 2) Fetch Discord user profile
            user_resp = requests.get(
                "https://discord.com/api/users/@me",
                headers={"Authorization": f"Bearer {discord_access}"}
            )
            if user_resp.status_code != 200:
                return Response(
                    {"detail": "Failed to fetch Discord user"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            discord_data = user_resp.json()

            # 3) Create or get local user by Discord ID
            user, _ = User.objects.get_or_create(
                discord_id=discord_data["id"],
                defaults={
                    "username": discord_data["username"],
                    # Ensure any non-nullable fields have defaults here
                }
            )

            # 4) Issue JWT tokens for this user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # 5) Return JWTs and user data in JSON
            return Response({
                "access": access_token,
                "refresh": refresh_token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "ultra_name": getattr(user, "ultra_name", None),
                    "level": getattr(user, "level", None),
                    "xp": getattr(user, "xp", None),
                    "rank": getattr(user, "rank", None),
                    "avatar_url": getattr(user, "avatar_url", None),
                },
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # Log exception and traceback for debugging
            print("❌ Exception in DiscordCallbackView:", e)
            traceback.print_exc()
            return Response(
                {"detail": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )