from django.contrib import admin

from finance_bot.langchain_bot.models import AgentSettings, AgentSettingsToUser


class AgentSettingsToUserInline(admin.StackedInline):
    model = AgentSettingsToUser


class AgentSettingsAdmin(admin.ModelAdmin):
    list_display = ('model', 'is_default',)
    inlines = [AgentSettingsToUserInline]


admin.site.register(AgentSettings, AgentSettingsAdmin)

