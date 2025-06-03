from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from finance_bot.users.models import User, UserInteraction


admin.site.register(User, UserAdmin)
admin.site.register(UserInteraction)
