from django.db import models

# Create your models here.


class Dialogue(models.Model):
    system_info = models.ForeignKey(
        "gpt_sys_info.SystemInfo",
        on_delete=models.SET_NULL,
        related_name="dialogue",
    )


class DialogueContent(models.Model):
    dialogue = models.ForeignKey(
        "dialogues.Dialogue",
        on_delete=models.CASCADE,
        related_name="contents",
    )
    number = models.PositiveSmallIntegerField()
    text = models.TextField()
