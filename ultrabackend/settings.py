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
    "corsheaders",                     # ← ganz oben, damit CORS funktioniert
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
    "corsheaders.middleware.CorsMiddleware",       # ← direkt nach Security
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
        "DIRS": [],
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
clean_url = raw_url.encode("utf-8", "ignore").decode("utf-8") if raw_url else None
DATABASES = {
    "default": dj_database_url.parse(
        clean_url,
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

# 🔐 Cookies & CSRF
SESSION_COOKIE_SECURE = USE_HTTPS
CSRF_COOKIE_SECURE = USE_HTTPS
SESSION_COOKIE_DOMAIN = None
SESSION_COOKIE_SAMESITE = "None" if USE_HTTPS else "Lax"
CSRF_COOKIE_SAMESITE = "None" if USE_HTTPS else "Lax"

# 🔐 Allauth & Discord Config
LOGIN_REDIRECT_URL = os.getenv("FRONTEND_LOGIN_REDIRECT", "http://localhost:5173/discord/callback").strip()
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

# ✅ Allauth + Signup without email
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_SIGNUP_FIELDS = ["username"]
ACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"

# 🔄 dj-rest-auth serializer config
REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "users.serializers.UserSerializer",
}

# 🌐 CORS & CSRF
CORS_ALLOW_CREDENTIALS = True
if USE_HTTPS:
    CORS_ALLOWED_ORIGINS = [
        "https://app.igoultra.de",       # ← deine Frontend-Domain
        "https://api.igoultra.de",       # optional: falls du Frontend und API mischst
    ]
    CSRF_TRUSTED_ORIGINS = [
        "https://app.igoultra.de",
        "https://api.igoultra.de",
    ]
else:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:5173",
        "http://localhost:8001",
    ]
    CSRF_TRUSTED_ORIGINS = [
        "http://localhost:5173",
        "http://localhost:8001",
    ]

# 📧 Dummy Email Backend
EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"
