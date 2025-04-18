"""
Django settings for ultrabackend project.
Generated by 'django-admin startproject' using Django 5.2.
"""

import os
import dj_database_url
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# --------------------------------------------
# 📁 Base Directory Setup
# --------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------
# 🔐 Secret Key & Debug Mode
# --------------------------------------------

# Load secret key from environment for security
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# Set debug mode from env, default to False for safety
DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"

# --------------------------------------------
# 🌍 Allowed Hosts
# --------------------------------------------

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "api.igoultra.de",
    ".herokuapp.com",
    "igoultra-backend-d20b10508b97.herokuapp.com",
]

# --------------------------------------------
# 🔑 Site Framework
# --------------------------------------------

SITE_ID = 1

# --------------------------------------------
# 🧩 Installed Applications
# --------------------------------------------

INSTALLED_APPS = [
    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # 3rd-party auth (Allauth + Discord)
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.discord',

    # REST Auth integration
    'dj_rest_auth',
    'dj_rest_auth.registration',

    # Useful dev/production tools
    'corsheaders',
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',

    # Local apps
    'users',
    'xp',
    'seasons',
]

# --------------------------------------------
# 🧱 Middleware Stack
# --------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # Whitenoise for static file serving in production
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --------------------------------------------
# 🔗 URL and WSGI Settings
# --------------------------------------------

ROOT_URLCONF = 'ultrabackend.urls'
WSGI_APPLICATION = 'ultrabackend.wsgi.application'

# --------------------------------------------
# 🎨 Templates Configuration
# --------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Add custom template dirs here if needed
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# --------------------------------------------
# 🛢️ PostgreSQL Database Configuration
# --------------------------------------------

DATABASES = {
    "default": dj_database_url.config(
        # Heroku uses DATABASE_URL automatically if available
        default=os.getenv("DATABASE_URL_LOCAL"),
        conn_max_age=600,  # Keeps DB connections open for 10 minutes
        ssl_require=not DEBUG,  # Enforce SSL in production only
    )
}

# --------------------------------------------
# 🔐 Password Validation
# --------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --------------------------------------------
# 🌐 Localization Settings
# --------------------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --------------------------------------------
# 📦 Static and Media Files Configuration
# --------------------------------------------

# URL to access static files (e.g., CSS, JS)
STATIC_URL = '/static/'

# Directory where collectstatic stores files for production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Enable WhiteNoise static file storage with caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Optional media file support (e.g., for uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --------------------------------------------
# 🧪 Miscellaneous Settings
# --------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
