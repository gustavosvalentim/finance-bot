import os

from typing import List, Type

from django.conf import settings
from langchain.agents import AgentExecutor
from langchain_openai.chat_models import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.utils import trim_messages
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool

from .base import BaseAgent, AgentError

from finance_bot.finance.constants import FINANCE_AGENT_NAME
from finance_bot.agents.loader import ClassLoader, ClassLoadingError


def pre_model_hook(state: dict, config: RunnableConfig) -> dict:
    """Hook to trim messages before LLM processing"""
    if not isinstance(state, dict) or "messages" not in state:
        return state

    trimmed_messages = trim_messages(
        state["messages"],
        max_tokens=48000,
        strategy="last",
        token_counter=ChatOpenAI(model='gpt-4o-mini'),
        start_on="human",
        allow_partial=False,
        include_system=True,
    )
    
    state.update({"messages": trimmed_messages})

    return state

class FinanceAgent(BaseAgent):
    """Finance-specific agent implementation"""

    def _load_tools(self) -> List[Type[BaseTool]]:
        """Load tools from configuration using ClassLoader"""
        agent_config = settings.AGENT_SETTINGS.get('agents', {}).get(FINANCE_AGENT_NAME, {})
        tool_paths = agent_config.get('tools', [])
        try:
            return ClassLoader.instantiate_classes(tool_paths)
        except ClassLoadingError as e:
            raise AgentError(f"Failed to load tools: {e}")
    
    def create_agent_executor(self) -> AgentExecutor:
        """Create LangChain agent executor for finance operations"""
        try:
            # Create language model
            model = ChatOpenAI(
                model=self.config.get('model', 'gpt-4o-mini'),
                api_key=os.getenv("OPENAI_API_KEY")
            )
            
            executor_params = {
                'model': model,
                'tools': self._load_tools(),
                'pre_model_hook': pre_model_hook,
            }
            
            if self.config.get('use_memory', False):
                executor_params['checkpointer'] = MemorySaver()
            
            agent = create_react_agent(**executor_params)

            return agent
            
        except Exception as e:
            raise AgentError(f"Failed to create finance agent executor: {e}")
