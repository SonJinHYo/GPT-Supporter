from django.db import models
from django.core.validators import MaxValueValidator


class PublicScript(models.Model):
    """공용 스크립트 모델"""

    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="user",
    )

    name = models.CharField(
        max_length=100,
        verbose_name="공용 스크립트 이름",
    )

    description = models.TextField(
        verbose_name="공용 스크립트 설명서",
        help_text="스크립트를 ChatGPT에게 전했을 때 효과, 이후 사용법 등 설명",
    )


class Script(models.Model):
    public_script = models.ForeignKey(
        "public_scripts.PublicScript",
        on_delete=models.CASCADE,
        related_name="scripts",
    )

    number = models.PositiveSmallIntegerField(
        verbose_name="스크립트 순번",
        validators=[
            MaxValueValidator(10, "최대 10개의 스크립트까지 가능합니다."),
        ],
    )

    text = models.TextField(
        verbose_name="스크립트",
        help_text="ChatGPT에게 전달할 스크립트",
    )
