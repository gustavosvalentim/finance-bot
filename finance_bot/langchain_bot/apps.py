from django.apps import AppConfig
from django.conf import settings

from finance_bot.langchain_bot.tool_manager import ToolManager


class LangchainBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'finance_bot.langchain_bot'

    def ready(self):
        ToolManager.instance().load_tools(settings.AGENT_SETTINGS['tools'])
