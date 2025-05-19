from .base import *

# ─── Production settings ─────────────────────────────────────────────────
DEBUG = False
USE_HTTPS = True

# Your public API domains
ALLOWED_HOSTS = [
    "api.igoultra.de",
    ".herokuapp.com",
]

# CORS & CSRF for production
CORS_ALLOWED_ORIGINS = [
    "https://app.igoultra.de",
    "https://www.igoultra.de",
    "https://api.igoultra.de",
]
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

# If you store media on S3, configure DEFAULT_FILE_STORAGE here
# If you send real emails, switch EMAIL_BACKEND to SMTP
