# Generated by Django 4.2 on 2023-08-16 08:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("chatrooms", "0003_chatroom_system_info_alter_chatroom_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="message",
            old_name="text",
            new_name="content",
        ),
        migrations.RenameField(
            model_name="message",
            old_name="sender",
            new_name="role",
        ),
    ]
