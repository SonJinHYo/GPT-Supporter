from .base import *

ALLOWED_HOSTS = ["0.0.0.0", "127.0.0.1", "localhost"]

WSGI_APPLICATION = "config.wsgi.local.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:3000", "http://127.0.0.1"]
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:3000", "http://127.0.0.1"]
