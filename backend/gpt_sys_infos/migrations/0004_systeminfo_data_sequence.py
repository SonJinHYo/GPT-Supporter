# Generated by Django 4.2 on 2023-08-16 03:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("gpt_sys_infos", "0003_alter_systeminfo_major"),
    ]

    operations = [
        migrations.AddField(
            model_name="systeminfo",
            name="data_sequence",
            field=models.BooleanField(default=False),
        ),
    ]
