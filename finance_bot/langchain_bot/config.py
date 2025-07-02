from typing import Dict, Any, Type, List

from django.conf import settings
from langchain_core.tools import BaseTool

from .models import AgentSettings, AgentSettingsToUser
from .tool_manager import ToolManager


class AgentConfiguration:
    """Service for retrieving agent configuration from database"""

    default_settings_queryset = AgentSettings.objects.filter(is_default=True)

    def __init__(self, tool_manager: ToolManager):
        self.tool_manager = tool_manager
    
    def get_agent_settings(self, user_id: str) -> Dict[str, Any]:
        """Get agent settings for a user without caching"""
        user_agent_settings = AgentSettingsToUser.objects.filter(
            user__id=user_id
        ).first()
        
        if user_agent_settings:
            agent_settings = user_agent_settings.agent_settings
        else:
            agent_settings = self.default_settings_queryset.first()
            
        if not agent_settings:
            raise ValueError("No agent settings found for user")
            
        return {
            'model': agent_settings.model,
            'prompt': agent_settings.prompt,
        }
    
    def get_tool_configurations(self) -> List[Type[BaseTool]]:
        """Get tools instances from settings"""
        return self.tool_manager.load_tools(settings.AGENT_SETTINGS.get('tools', []))
    
    def get_memory_configuration(self) -> bool:
        """Get memory configuration from settings"""
        return settings.AGENT_SETTINGS.get('use_memory', False) 
