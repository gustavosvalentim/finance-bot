# Generated by Django 5.1.7 on 2025-04-14 18:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=14)),
                ('name', models.CharField(max_length=255)),
                ('is_income', models.BooleanField(default=False)),
                ('limit', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=14)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.user')),
            ],
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('target_amount', models.FloatField(null=True)),
                ('current_amount', models.FloatField(null=True)),
                ('deadline', models.DateTimeField(null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.user')),
            ],
        ),
    ]
