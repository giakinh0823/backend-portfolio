# Generated by Django 4.0 on 2021-12-30 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0002_group_user_1_group_user_2'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='is_bot_run',
            field=models.BooleanField(default=True),
        ),
    ]
