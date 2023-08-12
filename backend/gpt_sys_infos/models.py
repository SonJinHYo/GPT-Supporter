from django.db import models

from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)


# Create your models here.
class SystemInfo(models.Model):
    LANGUAGES = [
        ("en", "English"),
        ("ko", "Korean"),
    ]

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="system_infos",
    )
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


class RefBook(models.Model):
    system_info = models.ForeignKey(
        "gpt_sys_infos.SystemInfo",
        null=True,
        on_delete=models.SET_NULL,
        related_name="ref_books",
    )
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=100)


class RefData(models.Model):
    system_info = models.ForeignKey(
        "gpt_sys_infos.SystemInfo",
        null=True,
        on_delete=models.SET_NULL,
        related_name="ref_datas",
    )
    title = models.CharField(max_length=100)


class Content(models.Model):
    data = models.OneToOneField(
        "gpt_sys_infos.RefData",
        on_delete=models.CASCADE,
        related_name="content",
    )
    text = models.TextField(max_length=2000)
