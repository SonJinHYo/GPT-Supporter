from django.db import models

from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)


class SystemInfo(models.Model):
    LANGUAGES = [
        ("en", "English"),
        ("ko", "Korean"),
    ]

    description = models.CharField(
        max_length=50,
        default="No Description",
        verbose_name="시스템 설정 설명",
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="system_infos",
    )
    language = models.CharField(
        max_length=2,
        choices=LANGUAGES,
        help_text="GPT의 답변 언어",
    )
    major = models.CharField(
        max_length=50,
        default=None,
        verbose_name="관련 전공",
        help_text="GPT에게 질문과 관련된 전공을 설정",
    )
    understanding_level = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0, message="대학교 기준입니다. 1~4학년 또는 석사 수준은 5학년을 선택해주세요"),
            MaxValueValidator(5, "대학교 기준입니다. 1~4학년 또는 석사 수준은 5학년을 선택해주세요"),
        ]
    )
    only_use_reference_data = models.BooleanField(
        default=False,
        help_text="사용자가 추가한 참고자료 위주로 답변 설정",
    )
    data_sequence = models.BooleanField(
        default=False,
        help_text="사용자의 참고자료 순서 존재 유무",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RefBook(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="ref_books",
    )

    system_info = models.ForeignKey(
        "gpt_sys_infos.SystemInfo",
        null=True,
        on_delete=models.SET_NULL,
        related_name="ref_books",
    )
    author = models.CharField(
        max_length=100,
        verbose_name="저자",
    )
    title = models.CharField(
        max_length=100,
        verbose_name="책 이름",
    )


class RefData(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="ref_datas",
    )

    system_info = models.ForeignKey(
        "gpt_sys_infos.SystemInfo",
        null=True,
        on_delete=models.SET_NULL,
        related_name="ref_datas",
    )
    title = models.CharField(
        max_length=100,
        verbose_name="참고자료 제목",
    )


class Content(models.Model):
    data = models.OneToOneField(
        "gpt_sys_infos.RefData",
        on_delete=models.CASCADE,
        related_name="content",
    )
    text = models.TextField(
        max_length=3000,
        verbose_name="참고자료 내용",
    )
