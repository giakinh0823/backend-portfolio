# Generated by Django 4.0 on 2021-12-17 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]