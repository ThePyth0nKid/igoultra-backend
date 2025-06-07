import os
from pathlib import Path
from datetime import timedelta

import dj_database_url
from dotenv import load_dotenv

# ─── Load environment variables ───────────────────────────────────────────────
load_dotenv()

# ─── Tell dj-rest-auth to use JWT only (no DRF Token model) ──────────────────
REST_USE_JWT = True
TOKEN_MODEL = None

# ─── Discord OAuth Credentials & Frontend Redirect ──────────────────────────
DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
FRONTEND_LOGIN_REDIRECT = os.getenv(
    "FRONTEND_LOGIN_REDIRECT",
    "http://localhost:5173/discord/callback"
).strip()
if not DISCORD_CLIENT_ID or not DISCORD_CLIENT_SECRET:
    raise RuntimeError(
        "❌ Please set DISCORD_CLIENT_ID and DISCORD_CLIENT_SECRET in your .env"
    )

# ─── Base directory & secret key ─────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# ─── Feature flags (override in local/prod) ─────────────────────────────────
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"
USE_HTTPS = os.getenv("USE_HTTPS", "False") == "True"

# ─── Hosts & CORS defaults (override per environment) ────────────────────────
ALLOWED_HOSTS = []
CORS_ALLOWED_ORIGINS = []
CSRF_TRUSTED_ORIGINS = []

# ─── Installed applications ─────────────────────────────────────────────────
INSTALLED_APPS = [
    "corsheaders",                      # must come before CommonMiddleware
    "whitenoise.runserver_nostatic",    # static file serving

    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    # Third-party auth & REST
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.discord",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",

    # API Documentation
    "drf_spectacular",

    # Developer utilities
    "django_extensions",

    # Local apps
    "users",
    "xp",
    "seasons",
]

SITE_ID = 1

# ─── Middleware ──────────────────────────────────────────────────────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",

    # Sessions & CSRF for Admin; API uses JWT only
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ultrabackend.urls"
WSGI_APPLICATION = "ultrabackend.wsgi.application"

# ─── Templates configuration ─────────────────────────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # project-wide template dirs
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",  # for admin & allauth
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ─── Database configuration ──────────────────────────────────────────────────
raw_db_url = os.getenv("DATABASE_URL_LOCAL") or os.getenv("DATABASE_URL")
if not raw_db_url:
    raise RuntimeError("DATABASE_URL_LOCAL or DATABASE_URL must be set")
clean_db_url = raw_db_url.encode("utf-8", "ignore").decode("utf-8")
DATABASES = {
    "default": dj_database_url.parse(
        clean_db_url,
        conn_max_age=600,
        ssl_require=USE_HTTPS,
    )
}

# ─── Custom user model ───────────────────────────────────────────────────────
AUTH_USER_MODEL = "users.User"

# ─── REST Framework: JWT authentication only for API ─────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    # Use drf-spectacular for schema generation
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# ─── drf-spectacular settings ────────────────────────────────────────────────
SPECTACULAR_SETTINGS = {
    "TITLE":       "iGoUltra API",
    "DESCRIPTION": "Interaktive API-Dokumentation (nur lokal)",
    "VERSION":     "1.0.0",
}

# ─── Simple JWT settings ─────────────────────────────────────────────────────
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),       # short-lived access tokens
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),      # longer-lived refresh tokens
    "ROTATE_REFRESH_TOKENS": True,                    # rotate & blacklist on use
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),                 # Authorization: Bearer <token>
}

# ─── Password validation ─────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ─── Internationalization ────────────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ─── Static & media files ────────────────────────────────────────────────────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ─── Session & CSRF defaults (overridden in local.py & production.py) ────────
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SAMESITE = "None"

# ─── Allauth & Discord OAuth configuration ──────────────────────────────────
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_PROVIDERS = {
    "discord": {
        "APP": {
            "client_id": DISCORD_CLIENT_ID,
            "secret": DISCORD_CLIENT_SECRET,
            "key": ""
        },
        "SCOPE": ["identify"],
    }
}
SOCIALACCOUNT_ADAPTER = "users.adapters.DiscordSocialAdapter"

# ─── Allauth signup settings ─────────────────────────────────────────────────
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_SIGNUP_FIELDS = ["username"]
ACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"

# ─── dj-rest-auth serializers override ───────────────────────────────────────
REST_AUTH_SERIALIZERS = {
    "SOCIAL_LOGIN_SERIALIZER": "users.serializers.DiscordJWTSerializer",
    "USER_DETAILS_SERIALIZER": "users.serializers.UserSerializer",
}

# ─── Email backend (dummy by default) ────────────────────────────────────────
EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"
