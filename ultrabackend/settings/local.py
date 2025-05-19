from .base import *

# ─── Development settings ─────────────────────────────────────────────────
DEBUG = True
USE_HTTPS = False

# Allow only localhost in dev
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# CORS & CSRF for local frontend
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:8001",
]
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

# Show emails in console rather than dummy
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
