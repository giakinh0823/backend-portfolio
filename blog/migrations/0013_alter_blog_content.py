# Generated by Django 4.0 on 2021-12-22 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_alter_blog_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=models.TextField(blank=True, null=True, unique=True),
        ),
    ]