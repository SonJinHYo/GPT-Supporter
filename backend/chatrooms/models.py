from django.db import models


class ChatRoom(models.Model):
    CATEGORYS = [
        ("general", "일반적인 질문"),
        ("equation", "수식 풀이"),
    ]

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="chatrooms",
    )
    name = models.CharField(max_length=50)
    category = models.CharField(
        max_length=20,
        choices=CATEGORYS,
        default="general",
    )
    system_info = models.OneToOneField(
        "gpt_sys_infos.SystemInfo",
        on_delete=models.CASCADE,
        related_name="system_info",
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    chatroom = models.ForeignKey(
        "chatrooms.ChatRoom",
        on_delete=models.CASCADE,
        related_name="messages",
    )
    role = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
