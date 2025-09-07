from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from finance_bot.users.models import User, UserInteraction


class CustomUserAdmin(UserAdmin):
    inlines = []


class CustomUserInteractionAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)
    list_display = ('user', 'interaction_type', 'interaction_data', 'created_at')
    search_fields = ('user__username', 'interaction_type', 'parent')


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserInteraction, CustomUserInteractionAdmin)
