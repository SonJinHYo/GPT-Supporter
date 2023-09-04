from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    "gpt-supporter.click",
]

WSGI_APPLICATION = "config.wsgi.prod.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",  # engine: mysql
        "NAME": "gs_db",  # DB Name
        "USER": "admin",  # DB User
        "PASSWORD": os.environ.get("AWS_DB_PASSWORD"),  # Password
        "HOST": os.environ.get("AWS_DB_HOST"),  # 생성한 데이터베이스 엔드포인트
        "PORT": "3306",  # 데이터베이스 포트
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

CORS_ALLOWED_ORIGINS = [
    "https://gpt-supporter.click",
]
CSRF_TRUSTED_ORIGINS = [
    "https://gpt-supporter.click",
]
