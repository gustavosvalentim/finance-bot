from django.contrib import admin

from finance_bot.users.models import User, UserInteraction


admin.site.register(User)
admin.site.register(UserInteraction)
