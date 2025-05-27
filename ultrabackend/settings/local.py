# settings/local.py
from .base import *

# ------------------------------------------------------------------------------
# Development settings
# ------------------------------------------------------------------------------
DEBUG = True
USE_HTTPS = False

# ------------------------------------------------------------------------------
# Hosts and CORS configuration for local development
# ------------------------------------------------------------------------------
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
]

# ------------------------------------------------------------------------------
# Allow cookies over CORS for Admin login
# ------------------------------------------------------------------------------
CORS_ALLOW_CREDENTIALS = True

# ------------------------------------------------------------------------------
# Cookie & CSRF settings for local development
# ------------------------------------------------------------------------------

# Do not require Secure flag on localhost
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Use Lax SameSite so cookies are sent on top-level navigation (e.g. Admin login form)
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"

# No domain restriction on localhost
SESSION_COOKIE_DOMAIN = None
CSRF_COOKIE_DOMAIN = None

# ------------------------------------------------------------------------------
# Email backend: console output for development
# ------------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
