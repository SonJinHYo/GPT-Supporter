from django.db import models


# 미사용 상태
class Dialogue(models.Model):
    system_info = models.ForeignKey(
        "gpt_sys_infos.SystemInfo",
        on_delete=models.SET_NULL,
        related_name="dialogue",
        null=True,
    )


class DialogueContent(models.Model):
    dialogue = models.ForeignKey(
        "dialogues.Dialogue",
        on_delete=models.CASCADE,
        related_name="contents",
    )
    number = models.PositiveSmallIntegerField(
        verbose_name="dialogue 정렬 기준",
    )
    text = models.TextField(
        verbose_name="dialogue 내용",
    )
