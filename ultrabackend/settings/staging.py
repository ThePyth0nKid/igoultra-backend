from .base import *

# ─── Staging/Pre-prod settings ────────────────────────────────────────────
DEBUG = False
USE_HTTPS = True

# Your staging domains
ALLOWED_HOSTS = ["staging.igoultra.de", ".herokuapp.com"]

# CORS & CSRF for staging
CORS_ALLOWED_ORIGINS = [
    "https://staging.igoultra.de",
    "https://api-staging.igoultra.de",
]
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

# Optionally add staging-only logging or error tracking here
