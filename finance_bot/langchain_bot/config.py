from typing import Dict, Any
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from .models import AgentSettings, AgentSettingsToUser


class AgentConfiguration:
    """Service for retrieving agent configuration from database"""

    @staticmethod
    def get_agent_settings(user_id: str) -> AgentSettings:
        """Get agent settings for a user"""
        try:
            # Try to get user-specific settings
            user_agent_settings = AgentSettingsToUser.objects.filter(
                user_id=user_id
            ).select_related('agent_settings').first()
            
            if user_agent_settings:
                return user_agent_settings.agent_settings
            
            # Fall back to default settings
            default_settings = AgentSettings.objects.filter(is_default=True).first()
            if not default_settings:
                # If no default settings, try to get any settings
                default_settings = AgentSettings.objects.first()
                if not default_settings:
                    raise ObjectDoesNotExist("No agent settings found in the database")
                    
            return default_settings
            
        except Exception as e:
            raise ValueError(f"Failed to load agent settings: {str(e)}")
    
    @staticmethod
    def get_agent_config(user_id: str) -> Dict[str, Any]:
        """Get complete agent configuration for a user"""
        try:
            settings = AgentConfiguration.get_agent_settings(user_id)
            
            # Get tools from settings or use empty list if not found
            tools_config = settings.tools if hasattr(settings, 'tools') else []
            
            return {
                'model': settings.model,
                'prompt': settings.prompt,
                'tools': tools_config,
                'use_memory': getattr(settings, 'use_memory', False)
            }
            
        except Exception as e:
            # Fallback to default configuration if available
            return {
                'model': 'gpt-4',
                'prompt': 'You are a helpful assistant.',
                'tools': [],
                'use_memory': False
            }
    
    @staticmethod
    def get_memory_configuration() -> bool:
        """Get memory configuration from settings"""
        return settings.AGENT_SETTINGS.get('use_memory', False)
