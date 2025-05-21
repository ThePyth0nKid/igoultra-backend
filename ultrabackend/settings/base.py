import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

# ─── Load environment variables from .env file ──────────────────────────────
load_dotenv()

# ─── BASE_DIR & Secret Key ──────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# ─── Feature flags (override in local/prod) ────────────────────────────────
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"
USE_HTTPS = os.getenv("USE_HTTPS", "False") == "True"

# ─── Hosts & CORS defaults (override per environment) ───────────────────────
ALLOWED_HOSTS = []  
CORS_ALLOWED_ORIGINS = []
CSRF_TRUSTED_ORIGINS = []

# ─── Installed Applications ─────────────────────────────────────────────────
INSTALLED_APPS = [
    # CORS & static file handling
    "corsheaders",
    "whitenoise.runserver_nostatic",

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

    # Developer utilities
    "django_extensions",

    # Local apps
    "users",
    "xp",
    "seasons",
]

SITE_ID = 1

# ─── Middleware ────────────────────────────────────────────────────────────
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

# ─── Templates ─────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # add project-wide template dirs here
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

# ─── Database Configuration ─────────────────────────────────────────────────
raw_db_url = os.getenv("DATABASE_URL_LOCAL") or os.getenv("DATABASE_URL")
if not raw_db_url:
    raise RuntimeError("DATABASE_URL_LOCAL or DATABASE_URL must be set")

# Strip any non-UTF8 bytes (e.g. BOM) so psycopg2 can parse correctly
clean_db_url = raw_db_url.encode("utf-8", "ignore").decode("utf-8")
DATABASES = {
    "default": dj_database_url.parse(
        clean_db_url,
        conn_max_age=600,
        ssl_require=USE_HTTPS,
    )
}

# ─── Authentication & REST Framework ────────────────────────────────────────
AUTH_USER_MODEL = "users.User"
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# ─── Password Validation ───────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ─── Internationalization ──────────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ─── Static & Media Files ──────────────────────────────────────────────────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ─── Session & CSRF (defaults, overridden per env) ─────────────────────────
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SAMESITE = "None"

# ─── Allauth & Discord OAuth Configuration ─────────────────────────────────
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

# ─── Allauth Signup Settings ───────────────────────────────────────────────
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_SIGNUP_FIELDS = ["username"]
ACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"

# ─── dj-rest-auth Serializers Override ─────────────────────────────────────
REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "users.serializers.UserSerializer",
}

# ─── Email Backend (can be overridden in prod) ──────────────────────────────
EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"
