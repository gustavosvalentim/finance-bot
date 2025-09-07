from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
    Custom user manager to handle user creation with email as the unique identifier.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('The Password field must be set for superusers')
        return self.create_user(email, password, is_superuser=True, is_staff=True, **extra_fields)


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

    objects = UserManager()

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
