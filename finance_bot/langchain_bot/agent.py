import os
from datetime import datetime, timedelta
from typing import Any

from django.conf import settings
from langchain.agents import create_react_agent
from langchain.memory import ConversationSummaryBufferMemory
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai.chat_models import ChatOpenAI

from finance_bot.langchain_bot.models import AgentSettings, AgentSettingsToUser
from finance_bot.module_utils import load_class


class FinanceAgent:
    agent_settings_cache = {}

    def __load_tools(self):
        return [(load_class(tool_loc)()) for tool_loc in settings.AGENT_SETTINGS['tools']]

    def __get_agent_settings(self, user_id: str, force_refresh: bool = False):
        cache_entry = self.agent_settings_cache.get(user_id)
        cache_expired = cache_entry is not None and datetime.now() > self.agent_settings_cache[user_id]['created_at'] + timedelta(minutes=30)
        if cache_entry is None or cache_expired or force_refresh:
            user_agent_settings_qs = AgentSettingsToUser.objects.filter(user__id=user_id)

            if user_agent_settings_qs.count() > 0:
                agent_settings = user_agent_settings_qs.first()
            else:
                agent_settings = AgentSettings.objects.filter(is_default=True).first()

            self.agent_settings_cache[user_id] = {
                'model': agent_settings.model,
                'prompt': agent_settings.prompt,
            }

        return self.agent_settings_cache[user_id]

    def __get_agent_executor(self, agent_settings: dict[str, Any], tools: list):
        model = ChatOpenAI(model=agent_settings.model, api_key=os.getenv("OPENAI_API_KEY"))
        
        agent_executor_params = {}

        if settings.AGENT_SETTINGS['use_memory']:
            agent_executor_params['checkpointer'] = ConversationSummaryBufferMemory(llm=model, max_token_limit=1000)

        return create_react_agent(model=model, tools=tools, **agent_executor_params)

    def load(self, user_id: str, user_nickname: str, force_refresh: bool = False) -> str:
        def create_invoker(agent_executor, config, system_prompt) -> str:
            def invoker(query):
                return agent_executor.invoke(
                    {'messages': [SystemMessage(content=system_prompt), HumanMessage(content=query)]},
                    config=config,
                )
            return invoker

        tools = self.__load_tools()
        agent_settings = self.__get_agent_settings(user_id, force_refresh)
        agent_executor = self.__get_agent_executor(agent_settings, tools)

        config = {
            'configurable': {
                'thread_id': user_id,
            }
        }

        system_prompt_formatted = agent_settings.prompt.format(
            user_id=user_id,
            user_nickname=user_nickname,
            now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        return create_invoker(agent_executor, config, system_prompt_formatted)

    def invoke(self, user_id: str, user_nickname: str, query: str) -> str:
        invoker = self.load(user_id, user_nickname)
        response = invoker(query)

        return response['messages'][-1].content
