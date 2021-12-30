# Generated by Django 4.0 on 2021-12-30 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0008_alter_group_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='is_news',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='group',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]