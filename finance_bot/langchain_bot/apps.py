from django.apps import AppConfig
from django.conf import settings

from finance_bot.langchain_bot.tool_manager import ToolManager

from finance_bot.agents.factory import AgentFactory
from finance_bot.agents.finance_agent import FinanceAgent
from finance_bot.finance.constants import FINANCE_AGENT_NAME


class LangchainBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'finance_bot.langchain_bot'

    def ready(self):
        ToolManager.instance().load_tools(settings.AGENT_SETTINGS['tools'])
