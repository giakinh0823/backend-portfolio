# Generated by Django 4.0 on 2021-12-18 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_topic_is_remove'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='removed',
            field=models.BooleanField(default=False),
        ),
    ]
