from typing import Dict, Type, List, Any
from .base import BaseAgent

class AgentFactory:
    """Registry-based factory for agent creation"""
    
    _registry: Dict[str, Type[BaseAgent]] = {}
    
    @classmethod
    def register_agent(cls, name: str, agent_class: Type[BaseAgent]) -> None:
        """Register an agent class with a name"""
        cls._registry[name] = agent_class
    
    @classmethod
    def create(cls, name: str, config: Dict[str, Any]) -> BaseAgent:
        """Create an agent instance by name"""
        if name not in cls._registry:
            available_agents = list(cls._registry.keys())
            raise ValueError(f"Agent '{name}' not registered. Available: {available_agents}")
        
        try:
            return cls._registry[name](config)
        except Exception as e:
            raise ValueError(f"Failed to create agent '{name}': {e}")
    
    @classmethod
    def list_agents(cls) -> List[str]:
        """List all registered agent names"""
        return list(cls._registry.keys())
