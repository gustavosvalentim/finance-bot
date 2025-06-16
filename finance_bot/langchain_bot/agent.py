import os

from datetime import datetime
from django.conf import settings
from finance_bot.langchain_bot.models import AgentSettings, AgentSettingsToUser
from finance_bot.module_utils import load_class
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from typing import Any


class FinanceAgent:
    memory = MemorySaver()
    default_config = {
        'configurable': {
            'thread_id': '1234567890',
        }
    }
    
    def __init__(self):
        self.tools = self.load_tools()

    def load_tools(self):
        return [(load_class(tool_loc)()) for tool_loc in settings.AGENT_SETTINGS['tools']]

    def invoke(self, user_id: str, user_nickname: str, query: str) -> (dict[str, Any] | Any):
        """Invoke the agent with the given query."""

        user_agent_settings = AgentSettingsToUser.objects.filter(user__id=user_id).first()
        agent_settings = AgentSettings.objects.filter(is_default=True)
        if user_agent_settings is not None:
            agent_settings = user_agent_settings.agent_settings
        else:
            agent_settings = agent_settings.first()

        # TODO: need to cache this model and agent executor
        # TODO: replace those instances only if model name changes
        # TODO: cache prompt and replace if changed from db
        model = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"], model=agent_settings.model)
        agent_executor = create_react_agent(model, self.tools, checkpointer=self.memory)

        system_prompt = agent_settings.prompt

        system_prompt_formatted = system_prompt.format(
            user_id=user_id,
            user_nickname=user_nickname,
            now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        return agent_executor.invoke(
            {'messages': [SystemMessage(content=system_prompt_formatted), HumanMessage(content=query)]},
            config=self.default_config,
        )
