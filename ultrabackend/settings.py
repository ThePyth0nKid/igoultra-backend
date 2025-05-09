import os
import dj_database_url
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"
USE_HTTPS = os.getenv("USE_HTTPS", "False") == "True"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "api.igoultra.de",
    ".herokuapp.com",
    "igoultra-backend-d20b10508b97.herokuapp.com",
]

# Proxy & HTTPS Settings
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
SECURE_SSL_REDIRECT = USE_HTTPS

# Installed apps
INSTALLED_APPS = [
    "corsheaders",  
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    # Third-party
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.discord",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "rest_framework",
    "rest_framework.authtoken",
    "django_extensions",
    "whitenoise.runserver_nostatic",

    # Local apps
    "users",
    "xp",
    "seasons",
]

SITE_ID = 1

# Middleware (CORS must be before SessionMiddleware)
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ultrabackend.urls"
WSGI_APPLICATION = "ultrabackend.wsgi.application"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # ggf. Pfade zu eigenen Templates
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Database
raw_url = os.getenv("DATABASE_URL_LOCAL") or os.getenv("DATABASE_URL")
if not raw_url:
    raise RuntimeError("❌ DATABASE_URL_LOCAL or DATABASE_URL is missing in your .env file")
DATABASES = {
    "default": dj_database_url.parse(
        raw_url,
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}

# Custom User Model
AUTH_USER_MODEL = "users.User"

# REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# Password Validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Localization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static & Media
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -----------------------------------------------------------------------------
# Cookies & CSRF: Production-only secure cross-domain config,
# lokal werden Django-Defaults (Secure=False, SameSite=Lax) verwendet.
# -----------------------------------------------------------------------------
if not DEBUG:
    # Secure & cross-domain cookies
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"
    CSRF_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_DOMAIN = ".igoultra.de"
    CSRF_COOKIE_DOMAIN = ".igoultra.de"

    # CORS & CSRF Trusted Origins
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOWED_ORIGINS = [
        "https://api.igoultra.de",
        "https://www.igoultra.de",
        "https://app.igoultra.de",
        "https://igoultra.de",
    ]
    CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS
else:
    # Local development: einfache Origins, Django-Defaults
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:5173",
        "http://localhost:8001",
    ]
    CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

# -----------------------------------------------------------------------------
# Allauth & Discord Config
# -----------------------------------------------------------------------------
LOGIN_REDIRECT_URL = os.getenv(
    "FRONTEND_LOGIN_REDIRECT",
    "http://localhost:5173/discord/callback"
).strip()

SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_PROVIDERS = {
    "discord": {
        "APP": {
            "client_id": os.getenv("DISCORD_CLIENT_ID"),
            "secret": os.getenv("DISCORD_CLIENT_SECRET"),
            "key": ""
        },
        "SCOPE": ["identify"],
    }
}
SOCIALACCOUNT_ADAPTER = "users.adapters.DiscordSocialAdapter"

ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_SIGNUP_FIELDS = ["username"]
ACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"

# dj-rest-auth serializers
REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "users.serializers.UserSerializer",
}

# Dummy E-Mail Backend
EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"
