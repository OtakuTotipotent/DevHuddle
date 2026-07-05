from datetime import timedelta
import os
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "django-insecure-x$vg*0_ylw(w!gi7rf*$(dzw$&(m01!r5ny7(dv5_$+f-mf5s8"
DEBUG = True
ALLOWED_HOSTS = []

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Apps / Parent Modules
INSTALLED_APPS = [
    "daphne",  # absolute top
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # My Apps
    "users",
    "feed",
    "intelligence",
    "communication",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

#  HTML & UI Layer
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Add custom context processor here:
                "feed.context_processors.unread_notifications_count",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database Layer
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Timezone
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Karachi"
USE_I18N = True
USE_TZ = True


# Static Files & Users Data
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"  # HTML side rendering
MEDIA_ROOT = BASE_DIR / "media"  # where files are stored

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "users.CustomUser"

# REDIRECTS
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

# ACCOUNT DELETION
ACCOUNT_DELETION_DELAY = timedelta(days=3)


# Prints email to terminal for/in DEV MODE
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# PRODUCTION MODE
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com' ...
#
# Activate the SMTP backend:
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = "DevHuddle Security <no-reply@devhuddle.com>"


# EXTERNAL APIs from ENVIRONMENT VARIABLES
GEMINI_API_KEY = env("GEMINI_API_KEY")


# Communication / Realtime Layer
ASGI_APPLICATION = "config.asgi.application"
# Zero-friction in-memory layer for development (Use Redis in Production)
CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}


# STRIPE PAYMENT GATEWAY
STRIPE_PUBLIC_KEY = env("STRIPE_PUBLIC_KEY", default="")
STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY", default="")
