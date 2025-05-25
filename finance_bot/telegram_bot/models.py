from django.db import models

from finance_bot.users.models import User


class TelegramUserSettings(models.Model):
    """
    TelegramUser model to store user information.
    """

    telegram_id = models.CharField(max_length=50, unique=True)
    rate_limit_enabled = models.BooleanField(default=True)
    rate_limit = models.IntegerField(default=100)

    def __str__(self):
        return self.telegram_id

    @staticmethod
    def create(telegram_id: str, name: str | None, email: str | None, phone: str | None, **kwargs):
        """
        Create a new TelegramUserSettings instance.
        """
        User.objects.get_or_create(
            email=email,
            name=name,
            phone=phone,
            telegram_id=telegram_id,
        )

        return TelegramUserSettings.objects.create(
            telegram_id=telegram_id,
            **kwargs
        )
