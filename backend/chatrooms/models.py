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
    name = models.CharField(max_length=20)
    category = models.CharField(
        max_length=20,
        choices=CATEGORYS,
        default="general",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    chatroom = models.ForeignKey(
        "chatrooms.ChatRoom",
        on_delete=models.CASCADE,
        related_name="messages",
    )
    sender = models.CharField(max_length=20)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
