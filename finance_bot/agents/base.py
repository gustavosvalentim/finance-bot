from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime
from langchain.agents import AgentExecutor
from langchain_core.messages import SystemMessage, HumanMessage


class AgentError(Exception):
    """Base exception for agent operations"""
    pass

class BaseAgent(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.agent_executor = self.create_agent_executor()
    
    def _format_prompt(self, prompt_template: str, context: Dict[str, Any]) -> str:
        """Format prompt template with context variables"""
        try:
            context['now'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return prompt_template.format(**context)
        except KeyError as e:
            raise AgentError(f"Missing required context key: {e}")

    @abstractmethod
    def create_agent_executor(self) -> AgentExecutor:
        """Create the underlying agent executor - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement create_agent_executor")
    
    def invoke(self, context: Dict[str, Any]) -> str:
        """Standard agent invocation - same for all agents"""
        try:
            required_keys = ['user_id', 'user_nickname', 'input']
            missing_keys = [key for key in required_keys if key not in context]
            if missing_keys:
                raise AgentError(f"Missing required context keys: {missing_keys}")
            
            prompt_template = self.config.get('prompt', '')
            system_prompt = self._format_prompt(prompt_template, context)
            
            response = self.agent_executor.invoke({
                'messages': [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=context['input'])
                ]
            }, config={'configurable': {'thread_id': context['user_id']}})
            
            return response['messages'][-1].content
            
        except Exception as e:
            if isinstance(e, AgentError):
                raise
            raise AgentError(f"Agent invocation failed: {e}")
