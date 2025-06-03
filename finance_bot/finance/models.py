from datetime import datetime
from django.db import models


class Category(models.Model):
    user = models.CharField(max_length=14)
    name = models.CharField(max_length=255)
    normalized_name = models.CharField(max_length=255, null=True)
    is_income = models.BooleanField(default=False)
    limit = models.FloatField(null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        self.normalized_name = self.name.upper()
        super().save(*args, **kwargs)


class Transaction(models.Model):
    user = models.CharField(max_length=14) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.FloatField(null=True)
    date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    description = models.TextField(null=True)
