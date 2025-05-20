#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    # ─── Always use the monolithic settings module ─────────────────────────────
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ultrabackend.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # If Django isn't installed or not on PYTHONPATH, raise a helpful error
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH? Did you activate your virtualenv?"
        ) from exc

    # Delegate to Django's CLI handler
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
