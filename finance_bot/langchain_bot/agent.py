from dataclasses import dataclass
import logging
import os

from datetime import datetime, timedelta
from django.conf import settings
from finance_bot.langchain_bot.models import AgentSettings, AgentSettingsToUser
from finance_bot.module_utils import load_class
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langgraph.prebuilt import create_react_agent
from typing import Any


@dataclass
class AgentSettingsCacheItem:
    id: int
    prompt: str
    model: str
    created_at: datetime


class FinanceAgent:
    default_config = {
        'configurable': {
            'thread_id': '1234567890',
        }
    }
    agent_settings_cache: dict[int, AgentSettingsCacheItem] = {}

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.tools = self.load_tools()
        self.model = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"], model="gpt-4o-mini")

    def load_tools(self):
        return [(load_class(tool_loc)()) for tool_loc in settings.AGENT_SETTINGS['tools']]

    def __get_agent_settings(self, user_id: str, force_refresh: bool = False):
        cache_expired = datetime.now() > self.agent_settings_cache[user_id] + timedelta(minutes=30)
        if user_id not in self.agent_settings_cache or cache_expired or force_refresh:
            user_agent_settings_qs = AgentSettingsToUser.objects.filter(user__id=user_id)

            if user_agent_settings_qs.count() > 0:
                agent_settings = user_agent_settings_qs.first()
            else:
                agent_settings = AgentSettings.objects.filter(is_default=True).first()

            self.agent_settings_cache[user_id] = AgentSettingsCacheItem(agent_settings.pk, agent_settings.prompt, agent_settings.model)

        return self.agent_settings_cache[user_id]

    def __get_agent_executor(self, agent_settings: AgentSettings):
        # TODO: need to cache this model and agent executor
        # TODO: replace those instances only if model name changes
        # TODO: cache prompt and replace if changed from db
        model = ChatOpenAI(api_key=os.environ.get("OPENAI_API_KEY"), model=agent_settings.model)
        
        agent_executor_params = {}

        if settings.AGENT_SETTINGS['use_memory']:
            agent_executor_params['checkpointer'] = ConversationSummaryBufferMemory(llm=model, max_token_limit=1000)

        return create_react_agent(model, self.tools, **agent_executor_params)

    def get_config(self, user_id: str) -> dict[str, Any]:
        config = self.default_config
        config.update({
            'configurable': {
                'thread_id': user_id,
            }
        })
        return config

    def invoke(self, user_id: str, user_nickname: str, query: str) -> (dict[str, Any] | Any):
        """Invoke the agent with the given query."""

        query = query.strip()
        agent_settings = self.__get_agent_settings(user_id, query.strip() == '/refresh')

        if query == "/refresh":
            self.logger.debug("Force cache refresh for user %s at %d", user_id, datetime.now())
            return "Cache was reset successfuly."
        
        agent_executor = self.__get_agent_executor(agent_settings)

        system_prompt_formatted = agent_settings.prompt.format(
            user_id=user_id,
            user_nickname=user_nickname,
            now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        config = self.get_config(user_id)
        response = agent_executor.invoke(
            {'messages': [SystemMessage(content=system_prompt_formatted), HumanMessage(content=query)]},
            config=config,
        )

        return response['messages'][-1].content
