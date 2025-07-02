from datetime import datetime
from typing import Any

from langchain.agents import AgentExecutor
from langchain_core.messages import SystemMessage, HumanMessage

from .config import AgentConfiguration
from .tool_manager import ToolManager, ToolLoadingError
from .agent_factory import AgentFactory, AgentCreationError


class FinanceAgentError(Exception):
    """Base exception for FinanceAgent errors"""
    pass


class FinanceAgent:
    """Main agent class that orchestrates all components"""

    def __init__(self):
        self.tool_manager = ToolManager()
        self.config_service = AgentConfiguration(self.tool_manager)
        self.agent_factory = AgentFactory()
    
    def _create_agent_invoker(self, agent_executor, config, system_prompt):
        """Create an invoker function for the agent"""
        def invoker(query: str):
            return agent_executor.invoke(
                {
                    'messages': [
                        SystemMessage(content=system_prompt), 
                        HumanMessage(content=query)
                    ]
                },
                config=config,
            )
        return invoker
    
    def _format_system_prompt(self, prompt_template: str, user_id: str, user_nickname: str) -> str:
        """Format the system prompt with user context"""
        return prompt_template.format(
            user_id=user_id,
            user_nickname=user_nickname,
            now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
    
    def load(self, user_id: str, user_nickname: str) -> (AgentExecutor, str):
        """Load and configure an agent for the given user"""
        try:
            agent_settings = self.config_service.get_agent_settings(user_id)
            tools = self.config_service.get_tool_configurations()
            use_memory = self.config_service.get_memory_configuration()
            
            agent_executor = self.agent_factory.create_agent(
                agent_settings, 
                tools, 
                use_memory
            )
            
            system_prompt = self._format_system_prompt(
                agent_settings['prompt'], 
                user_id, 
                user_nickname
            )
            
            return agent_executor, system_prompt
        except (ToolLoadingError, AgentCreationError) as e:
            raise FinanceAgentError(f"Failed to load agent: {str(e)}")
        except Exception as e:
            raise FinanceAgentError(f"Unexpected error loading agent: {str(e)}")
    
    def invoke(self, user_id: str, user_nickname: str, query: str) -> str:
        """Invoke the agent with a query"""
   
        config = {
            'configurable': {
                'thread_id': user_id,
            }
        }

        try:
            agent_executor, system_prompt = self.load(user_id, user_nickname)

            response = agent_executor.invoke(
                {
                    'messages': [
                        SystemMessage(content=system_prompt), 
                        HumanMessage(content=query)
                    ]
                },
                config=config,
            )

            return response['messages'][-1].content
        except FinanceAgentError:
            raise
        except Exception as e:
            raise FinanceAgentError(f"Failed to invoke agent: {str(e)}")
