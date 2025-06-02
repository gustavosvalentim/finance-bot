from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class User(AbstractUser):
    """
    User model to store user information.
    """

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150, blank=True, null=True)

    # Overrides from AbstractUser
    username = models.CharField(max_length=150, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name

class UserInteraction(models.Model):
    """
    User interaction model to store user interactions with the bot.
    """

    class InteractionType(models.TextChoices):
        MESSAGE = "message", "Message"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=50)
    interaction_type = models.CharField(max_length=7, choices=InteractionType.choices)
    interaction_data = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.interaction_type}"
