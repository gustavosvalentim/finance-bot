from django.db import models

from finance_bot.users.models import User


class TelegramUserSettings(models.Model):
    """
    TelegramUser model to store user information.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    telegram_id = models.CharField(max_length=50, unique=True)
    rate_limit_enabled = models.BooleanField(default=True)
    rate_limit = models.IntegerField(default=100)

    class Meta:
        verbose_name = "User settings (Telegram)"
        verbose_name_plural = "User settings (Telegram)"

    def __str__(self):
        return self.telegram_id
