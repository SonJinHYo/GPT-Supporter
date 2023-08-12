from django.db import models


class ChatRoom(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="chatrooms",
    )
    name = models.CharField(max_length=20)
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
