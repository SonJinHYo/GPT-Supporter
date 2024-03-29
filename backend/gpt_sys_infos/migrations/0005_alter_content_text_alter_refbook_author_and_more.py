# Generated by Django 4.2 on 2023-09-01 16:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("gpt_sys_infos", "0004_systeminfo_data_sequence"),
    ]

    operations = [
        migrations.AlterField(
            model_name="content",
            name="text",
            field=models.TextField(max_length=3000, verbose_name="참고자료 내용"),
        ),
        migrations.AlterField(
            model_name="refbook",
            name="author",
            field=models.CharField(max_length=100, verbose_name="저자"),
        ),
        migrations.AlterField(
            model_name="refbook",
            name="title",
            field=models.CharField(max_length=100, verbose_name="책 이름"),
        ),
        migrations.AlterField(
            model_name="refdata",
            name="title",
            field=models.CharField(max_length=100, verbose_name="참고자료 제목"),
        ),
        migrations.AlterField(
            model_name="systeminfo",
            name="data_sequence",
            field=models.BooleanField(default=False, help_text="사용자의 참고자료 순서 존재 유무"),
        ),
        migrations.AlterField(
            model_name="systeminfo",
            name="description",
            field=models.CharField(
                default="No Description", max_length=50, verbose_name="시스템 설정 설명"
            ),
        ),
        migrations.AlterField(
            model_name="systeminfo",
            name="language",
            field=models.CharField(
                choices=[("en", "English"), ("ko", "Korean")],
                help_text="GPT의 답변 언어",
                max_length=2,
            ),
        ),
        migrations.AlterField(
            model_name="systeminfo",
            name="major",
            field=models.CharField(
                default=None,
                help_text="GPT에게 질문과 관련된 전공을 설정",
                max_length=50,
                verbose_name="관련 전공",
            ),
        ),
        migrations.AlterField(
            model_name="systeminfo",
            name="only_use_reference_data",
            field=models.BooleanField(
                default=False, help_text="사용자가 추가한 참고자료 위주로 답변 설정"
            ),
        ),
        migrations.AlterField(
            model_name="systeminfo",
            name="understanding_level",
            field=models.PositiveIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(
                        0, message="대학교 기준입니다. 1~4학년 또는 석사 수준은 5학년을 선택해주세요"
                    ),
                    django.core.validators.MaxValueValidator(
                        5, "대학교 기준입니다. 1~4학년 또는 석사 수준은 5학년을 선택해주세요"
                    ),
                ]
            ),
        ),
    ]
