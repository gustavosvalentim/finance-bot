from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class User(AbstractUser):
    """
    User model to store user information.
    """

    username = None

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

class UserInteraction(models.Model):
    """
    User interaction model to store user interactions with the bot.
    """

    class InteractionType(models.TextChoices):
        MESSAGE = "message", "Message"
        RESPONSE = "response", "Response"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=50)
    interaction_type = models.CharField(max_length=8, choices=InteractionType.choices)
    interaction_data = models.TextField(blank=True, default="")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        display_str = f"{self.user.first_name} {self.user.last_name} - {self.interaction_type} from {self.source}"
        if self.parent:
            display_str += " (reply)"
        return display_str
