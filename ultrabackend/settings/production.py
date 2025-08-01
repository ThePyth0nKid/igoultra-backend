from .base import *
import os

# ─── Production settings ────────────────────────────────────────────────────
DEBUG = False
USE_HTTPS = True
# Enable credentialed CORS
CORS_ALLOW_CREDENTIALS = True

# ─── Allowed Hosts ──────────────────────────────────────────────────────────
ALLOWED_HOSTS = [
    "api.igoultra.de",
    ".herokuapp.com",
]

# ─── HTTPS & Proxy Settings ─────────────────────────────────────────────────
# Trust X-Forwarded headers from Heroku router
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
SECURE_SSL_REDIRECT = True  # Redirect all HTTP to HTTPS

# ─── CORS & CSRF Origins ────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = [
    "https://app.igoultra.de",
    "https://www.igoultra.de",
    "https://api.igoultra.de",
]
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

# ─── Secure Cookies & CSRF Settings ─────────────────────────────────────────
SESSION_COOKIE_SECURE = True    # Only send session cookie over HTTPS
CSRF_COOKIE_SECURE = True       # Only send CSRF cookie over HTTPS

SESSION_COOKIE_SAMESITE = "None"  # Allow cross-site cookie sending
CSRF_COOKIE_SAMESITE = "None"     # Allow cross-site cookie sending

SESSION_COOKIE_DOMAIN = ".igoultra.de"  # Cookies valid for all subdomains
CSRF_COOKIE_DOMAIN = ".igoultra.de"

# ─── Allauth & Discord OAuth Redirect ───────────────────────────────────────
LOGIN_REDIRECT_URL = os.getenv(
    "FRONTEND_LOGIN_REDIRECT",
    "https://app.igoultra.de/discord/callback"
).strip()

# ─── Inject Discord OAuth credentials from environment ───────────────────────
SOCIALACCOUNT_PROVIDERS["discord"]["APP"]["client_id"] = os.getenv("DISCORD_CLIENT_ID")
SOCIALACCOUNT_PROVIDERS["discord"]["APP"]["secret"] = os.getenv("DISCORD_CLIENT_SECRET")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")

# ─── AWS S3 Configuration ────────────────────────────────────────────────────
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}