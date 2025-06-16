from django.contrib import admin

from finance_bot.telegram_bot.models import TelegramUserSettings
from finance_bot.users.admin import CustomUserAdmin


class TelegramUserSettingsInline(admin.TabularInline):
    model = TelegramUserSettings
    can_delete = False


CustomUserAdmin.inlines.append(TelegramUserSettingsInline)
