from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MinLengthValidator,
)


class User(AbstractUser):
    username = models.CharField(
        max_length=20,
        unique=True,
    )
    email = models.EmailField()
    password = models.CharField(
        max_length=128,
        validators=[MinLengthValidator(8)],
    )
    using_token = models.PositiveIntegerField(
        default=0,
        verbose_name="사용한 토큰량",
        help_text="실질적으로 대화형 GPT 서비스를 직접 사용할 때 사용합니다.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
