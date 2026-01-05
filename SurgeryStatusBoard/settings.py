"""
Django settings for SurgeryStatusBoard project.
"""

import os
from datetime import timedelta
from pathlib import Path

import dj_database_url

# --- BASE CONFIG -------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "django-insecure-eziee%xhld*yfgyr)!)7d%1iuze0e*0l-m1rjgn!$g4w-p0ngi"
DEBUG = os.getenv("DEBUG", "False") == "True"

# we define ALLOWED_HOSTS to accept all hosts for development purposes cause we dont know hat url will be after deployment
ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()]

# --- APPLICATIONS ------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "corsheaders",
    "rest_framework",
    # Local apps
    "accounts",
    "tracker",
]

# --- MIDDLEWARE --------------------------------------------------------------

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "SurgeryStatusBoard.urls"

# --- TEMPLATES ---------------------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "SurgeryStatusBoard.wsgi.application"

# --- DATABASE ---------------------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    # Local development fallback
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "ssb_db",
            "USER": "ssb_user",
            "PASSWORD": "gazal18100",
            "HOST": "localhost",
            "PORT": "5432",
        }
    }


# --- AUTHENTICATION ----------------------------------------------------------

AUTH_USER_MODEL = "accounts.CustomUser"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

# --- SIMPLE JWT CONFIGURATION ------------------------------------------------

from datetime import timedelta

SIMPLE_JWT = {
    # ⏰ Extend access token lifetime (default is 5 minutes)
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=12),
    # ♻️ Extend refresh token lifetime
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    # 🔄 Token rotation and blacklisting
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    # ⚙️ Header settings
    "AUTH_HEADER_TYPES": ("Bearer",),
    # Optional but good to keep these defaults explicit
    "UPDATE_LAST_LOGIN": False,
}

# --- PASSWORD VALIDATORS ----------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- INTERNATIONALIZATION ----------------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- STATIC FILES ------------------------------------------------------------
STATIC_URL = "/static/"

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- EMAIL CONFIG ------------------------------------------------------------

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "apikey"  # This literally stays "apikey"
EMAIL_HOST_PASSWORD = os.getenv("SENDGRID_API_KEY")
DEFAULT_FROM_EMAIL = "ahmadshamurannba@gmail.com"

# --- FRONTEND & CORS ---------------------------------------------------------

FRONTEND_URL = "https://ssb-delta.vercel.app"

CORS_ALLOWED_ORIGINS = [
    FRONTEND_URL,
]

CORS_ALLOW_CREDENTIALS = True
