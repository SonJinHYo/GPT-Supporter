from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MinLengthValidator,
    MinValueValidator,
    MaxValueValidator,
)


class User(AbstractUser):
    username = models.CharField(
        max_length=20,
    )
    email = models.EmailField()
    password = models.CharField(
        max_length=128,
        validators=[MinLengthValidator(8)],
    )
    using_token = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SystemInfo(models.Model):
    LANGUAGES = [
        ("en", "English"),
        ("ko", "Korean"),
    ]

    language = models.CharField(max_length=2, choices=LANGUAGES)
    major = models.CharField(max_length=20)
    understanding_level = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0, message="대학교 기준입니다. 1~5학년을 선택해주세요"),
            MaxValueValidator(5, "대학교 기준입니다. 1~5학년을 선택해주세요"),
        ]
    )
    only_use_reference_data = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
