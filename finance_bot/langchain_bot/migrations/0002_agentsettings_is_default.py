# Generated by Django 5.1.7 on 2025-06-12 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('langchain_bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentsettings',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
    ]
