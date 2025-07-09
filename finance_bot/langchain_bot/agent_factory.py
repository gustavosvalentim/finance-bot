import os

from typing import List, Any, Dict, Type
from langchain_core.tools import BaseTool
from langchain_openai.chat_models import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.utils import (
    trim_messages,
    count_tokens_approximately
)


def pre_model_hook(state):
    trimmed_messages = trim_messages(
        state["messages"],
        max_tokens=48000,
        strategy="last",
        token_counter=count_tokens_approximately,
        start_on="human",
        allow_partial=False,
        include_system=True,
    )

    state.update({ 'messages': trimmed_messages })

    return state


class AgentCreationError(Exception):
    """Exception raised when agent creation fails"""
    pass


class AgentFactory:
    """Factory for creating LangChain agents"""

    memory = None
    
    def create_agent(self, agent_settings: Dict[str, Any], tools: List[Type[BaseTool]], use_memory: bool = False):
        """Create a LangChain agent with the given configuration"""
        try:
            # Create the language model
            model = ChatOpenAI(
                model=agent_settings['model'], 
                api_key=os.getenv("OPENAI_API_KEY")
            )
            
            # Configure agent executor parameters
            agent_executor_params = {}
            
            if use_memory:
                self.memory = self.memory or MemorySaver()
                agent_executor_params['checkpointer'] = self.memory

            # Create the agent
            agent_executor = create_react_agent(
                model=model, 
                tools=tools,
                pre_model_hook=pre_model_hook,
                **agent_executor_params
            )
            
            return agent_executor
            
        except Exception as e:
            raise AgentCreationError(f"Failed to create agent: {str(e)}") 
