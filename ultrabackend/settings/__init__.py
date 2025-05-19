import os

# Determine the current running environment; default to 'local' if DJANGO_ENV is not set.
env = os.getenv('DJANGO_ENV', 'local')

# Load environment-specific settings modules based on DJANGO_ENV value.
if env == 'production':
    # In production, import all settings from production.py
    from .production import *
elif env == 'staging':
    # In staging (pre-production/testing), import all settings from staging.py
    from .staging import *
else:
    # For any other environment (including 'local'), import local development settings
    from .local import *
