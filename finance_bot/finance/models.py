from datetime import datetime
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=14)
    created_at = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    user = models.CharField(max_length=14)
    name = models.CharField(max_length=255)
    is_income = models.BooleanField(default=False)
    limit = models.FloatField(null=True)


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    target_amount = models.FloatField(null=True)
    current_amount = models.FloatField(null=True)
    deadline = models.DateTimeField(null=True)


class Transaction(models.Model):
    user = models.CharField(max_length=14) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.FloatField(null=True)
    date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    description = models.TextField(null=True)
