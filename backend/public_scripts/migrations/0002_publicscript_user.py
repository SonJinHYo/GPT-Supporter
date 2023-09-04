# Generated by Django 4.2 on 2023-09-02 06:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("public_scripts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="publicscript",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]