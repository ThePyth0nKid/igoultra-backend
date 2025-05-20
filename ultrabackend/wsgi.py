"""
WSGI config for ultrabackend project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
from django.core.wsgi import get_wsgi_application

# ─── Determine the current environment ───────────────────────────────────────
# Read DJANGO_ENV (e.g. "local", "staging", "production"), default to "local"
env = os.getenv("DJANGO_ENV", "local").lower()

# ─── Compute the settings module path ───────────────────────────────────────
# This will resolve to:
#   "ultrabackend.settings.local"      in development
#   "ultrabackend.settings.staging"    in your staging server
#   "ultrabackend.settings.production" in production
settings_module = f"ultrabackend.settings.{env}"

# ─── Ensure Django uses the correct settings ───────────────────────────────
# Only set DJANGO_SETTINGS_MODULE if it isn’t already defined
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

# ─── Create the WSGI application callable ─────────────────────────────────
# The WSGI server (Gunicorn/uWSGI) will use this "application" object to serve requests.
application = get_wsgi_application()
