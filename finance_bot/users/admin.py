from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from finance_bot.users.models import User, UserInteraction


class CustomUserAdmin(UserAdmin):
    inlines = []


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserInteraction)
