from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    "0.0.0.0",
    "127.0.0.1",
    "localhost",
    "ecs-alb-1087560193.ap-northeast-2.elb.amazonaws.com",
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
    "http://127.0.0.1:3000",
    "http://127.0.0.1",
    "http://ecs-alb-1087560193.ap-northeast-2.elb.amazonaws.com",
]
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:3000",
    "http://127.0.0.1",
    "http://ecs-alb-1087560193.ap-northeast-2.elb.amazonaws.com",
]
