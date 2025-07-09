from typing import Dict, Any
from django.conf import settings
from finance_bot.langchain_bot.models import AgentSettings, AgentSettingsToUser

class ConfigurationError(Exception):
    """Raised when configuration is invalid"""
    pass

class AgentConfiguration:
    """Manages agent configuration loading and validation"""
    
    @staticmethod
    def get_agent_config(user_id: str) -> Dict[str, Any]:
        """Get agent configuration for a user"""
        try:
            # Get user-specific settings or default
            user_settings = AgentSettingsToUser.objects.filter(user__id=user_id).first()
            
            if user_settings:
                agent_settings = user_settings.agent_settings
            else:
                agent_settings = AgentSettings.objects.filter(is_default=True).first()
            
            if not agent_settings:
                raise ConfigurationError("No agent settings found")
            
            # Build configuration dict
            config = {
                'model': agent_settings.model,
                'prompt': agent_settings.prompt,
                'tools': settings.AGENT_SETTINGS.get('tools', []),
                'use_memory': settings.AGENT_SETTINGS.get('use_memory', False)
            }
            
            return config
            
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {e}")
