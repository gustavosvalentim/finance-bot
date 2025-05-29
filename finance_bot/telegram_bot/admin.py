from django.contrib import admin

from finance_bot.telegram_bot.models import TelegramUserSettings
from finance_bot.users.models import UserInteraction


admin.site.register(TelegramUserSettings)
admin.site.register(UserInteraction)
