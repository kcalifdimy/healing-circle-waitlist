"""
Django settings for the Healing Circle waitlist project.

Email credentials are read from environment variables so you never
commit secrets. See README.md for the exact variables to set.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load variables from the .env file sitting next to manage.py
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-only-insecure-key-change-me-in-production",
)

DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "waitlist",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "healingcircle.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "healingcircle.wsgi.application"

# No database needed for this simple flow — signups are emailed, not stored.
DATABASES = {}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


STATIC_ROOT = BASE_DIR / "staticfiles"        # collectstatic gathers files here
STATICFILES_DIRS = [BASE_DIR / "static"]      # your source CSS/JS/images go here
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ---------------------------------------------------------------------------
# Email configuration — values come from the .env file (see .env.example)
# ---------------------------------------------------------------------------
# NOTE: for Gmail, EMAIL_HOST_PASSWORD must be an App Password
# (Google Account -> Security -> App passwords), not your normal password.
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "1") == "1"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

# Where waitlist signup notifications are sent — YOUR email address.
WAITLIST_NOTIFY_EMAIL = os.environ.get("WAITLIST_NOTIFY_EMAIL", EMAIL_HOST_USER)

# Fail fast with a clear message instead of a cryptic SMTPAuthenticationError
# if someone forgot to fill in .env.
_PLACEHOLDER_VALUES = {"", "you@gmail.com", "your-app-password"}
if EMAIL_HOST_USER in _PLACEHOLDER_VALUES or EMAIL_HOST_PASSWORD in _PLACEHOLDER_VALUES:
    import warnings
    warnings.warn(
        "EMAIL_HOST_USER / EMAIL_HOST_PASSWORD look like placeholder values. "
        "Edit the .env file next to manage.py with your real Gmail address "
        "and App Password, then restart the server.",
        stacklevel=2,
    )
