"""
WSGI config for ultrabackend project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
from django.core.wsgi import get_wsgi_application

# ─── Always use the monolithic settings module ─────────────────────────────
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ultrabackend.settings")

# Create the WSGI application callable for the web server
application = get_wsgi_application()
