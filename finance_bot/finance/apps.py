from django.apps import AppConfig

from finance_bot.agents.factory import AgentFactory
from finance_bot.agents.finance_agent import FinanceAgent
from finance_bot.finance.constants import FINANCE_AGENT_NAME


class FinanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'finance_bot.finance'

    def ready(self):
        AgentFactory.register_agent(FINANCE_AGENT_NAME, FinanceAgent)
