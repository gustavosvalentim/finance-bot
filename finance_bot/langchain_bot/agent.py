from dataclasses import dataclass
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


@dataclass
class AgentSettingsCacheItem:
    id: int
    prompt: str
    model: str


class FinanceAgent:
    memory = MemorySaver()
    default_config = {
        'configurable': {
            'thread_id': '1234567890',
        }
    }
    agent_settings_cache: dict[int, AgentSettingsCacheItem] = {}

    def __init__(self):
        self.tools = self.load_tools()

    def load_tools(self):
        return [(load_class(tool_loc)()) for tool_loc in settings.AGENT_SETTINGS['tools']]

    def __get_agent_settings(self, user_id: str):
        if user_id not in self.agent_settings_cache:
            user_agent_settings = AgentSettingsToUser.objects.filter(user__id=user_id).first()
            agent_settings = AgentSettings.objects.filter(is_default=True)

            if user_agent_settings is not None:
                agent_settings = user_agent_settings.agent_settings
            else:
                agent_settings = agent_settings.first()

            self.agent_settings_cache[user_id] = AgentSettingsCacheItem(agent_settings.pk, agent_settings.prompt, agent_settings.model)

        return self.agent_settings_cache[user_id]

    def __get_agent_executor(self, agent_settings: AgentSettings):
        # TODO: need to cache this model and agent executor
        # TODO: replace those instances only if model name changes
        # TODO: cache prompt and replace if changed from db
        model = ChatOpenAI(api_key=os.environ.get("OPENAI_API_KEY"), model=agent_settings.model)
        return create_react_agent(model, self.tools, checkpointer=self.memory)

    def invoke(self, user_id: str, user_nickname: str, query: str) -> str:
        """Invoke the agent with the given query."""

        query = query.strip()
        agent_settings = self.agent_settings_cache.get(user_id)

        if agent_settings is None or query == "/refresh": # TODO: commands is bad
            agent_settings = self.__get_agent_settings(user_id)

        if query == "/refresh":
            return "Cache was reset successfuly."
        
        agent_executor = self.__get_agent_executor(agent_settings)

        system_prompt_formatted = agent_settings.prompt.format(
            user_id=user_id,
            user_nickname=user_nickname,
            now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        response = agent_executor.invoke(
            {'messages': [SystemMessage(content=system_prompt_formatted), HumanMessage(content=query)]},
            config=self.default_config,
        )

        return response['messages'][-1].content
