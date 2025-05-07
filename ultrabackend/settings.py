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
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"

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
# 🔒 Heroku SSL Support
# --------------------------------------------
USE_HTTPS = os.getenv("USE_HTTPS", "False") == "True"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
SECURE_SSL_REDIRECT = USE_HTTPS  # Redirect all HTTP to HTTPS

# --------------------------------------------
# 🧩 Installed Applications
# --------------------------------------------
INSTALLED_APPS = [
    # Core Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    # Third-party apps
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.discord",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "django_extensions",
    "whitenoise.runserver_nostatic",

    # Local apps
    "users",
    "xp",
    "seasons",
]

# --------------------------------------------
# 🧱 Middleware Stack
# --------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "users.middleware.EnsureProfileComplete",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --------------------------------------------
# 🔗 URL & WSGI Settings
# --------------------------------------------
ROOT_URLCONF = "ultrabackend.urls"
WSGI_APPLICATION = "ultrabackend.wsgi.application"

# --------------------------------------------
# 🎨 Templates Configuration
# --------------------------------------------
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

# --------------------------------------------
# 🛢️ Database (PostgreSQL on Heroku)
# --------------------------------------------
raw_url = os.getenv("DATABASE_URL_LOCAL") or os.getenv("DATABASE_URL")
clean_url = raw_url.encode("utf-8", "ignore").decode("utf-8") if raw_url else None

DATABASES = {
    "default": dj_database_url.parse(
        clean_url,
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}

# --------------------------------------------
# 🔐 Password Validation
# --------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------------------------------
# 🌐 Internationalization
# --------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --------------------------------------------
# 📦 Static & Media Files
# --------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --------------------------------------------
# ⚙️ Miscellaneous
# --------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "users.User"

# --------------------------------------------
# 🔐 REST Framework (Session Auth Only)
# --------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# --------------------------------------------
# 🍪 Cookie & CSRF Configuration
# --------------------------------------------
SESSION_COOKIE_SECURE = USE_HTTPS
CSRF_COOKIE_SECURE = USE_HTTPS
SESSION_COOKIE_DOMAIN = "api.igoultra.de" if USE_HTTPS else None
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False  # Required for some JavaScript-based setups

if USE_HTTPS:
    SESSION_COOKIE_SAMESITE = "None"
    CSRF_COOKIE_SAMESITE = "None"
else:
    SESSION_COOKIE_SAMESITE = "Lax"
    CSRF_COOKIE_SAMESITE = "Lax"

# --------------------------------------------
# 🔐 Allauth & Social Login Settings
# --------------------------------------------
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_AUTHENTICATION_METHOD = "username"
LOGIN_REDIRECT_URL = "/"

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

# --------------------------------------------
# 🌐 CORS & CSRF Trusted Origins
# --------------------------------------------
if USE_HTTPS:
    CORS_ALLOWED_ORIGINS = ["https://api.igoultra.de"]
    CSRF_TRUSTED_ORIGINS = ["https://api.igoultra.de"]
else:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:5173",
        "http://localhost:8001",
    ]
    CSRF_TRUSTED_ORIGINS = [
        "http://localhost:5173",
        "http://localhost:8001",
    ]

# --------------------------------------------
# 📧 Email Backend (for development)
# --------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"
