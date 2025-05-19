#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # ─── Determine target settings module based on DJANGO_ENV ──────────────────
    # If DJANGO_ENV is not set, default to 'local'
    env = os.getenv("DJANGO_ENV", "local").lower()

    # Construct the full Python path to the settings module,
    # e.g. "ultrabackend.settings.local" or "ultrabackend.settings.production"
    settings_module = f"ultrabackend.settings.{env}"

    # Set the DJANGO_SETTINGS_MODULE if not already defined
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # If Django isn’t installed or not on PYTHONPATH, bail out with a helpful message
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH? Did you activate your virtualenv?"
        ) from exc

    # Delegate to Django's CLI handler
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
