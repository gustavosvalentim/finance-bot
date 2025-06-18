from django.contrib import admin

from finance_bot.telegram_bot.models import TelegramUserSettings


admin.site.register(TelegramUserSettings)
