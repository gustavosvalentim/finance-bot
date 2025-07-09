import os
import unittest
from unittest.mock import patch, MagicMock, ANY
from django.test import TestCase
from django.conf import settings

from .loader import ClassLoader, ClassLoadingError
from .factory import AgentFactory
from .finance_agent import FinanceAgent
from .config import AgentConfiguration, ConfigurationError


class TestClassLoader(unittest.TestCase):
    def test_load_valid_class(self):
        """Test loading a valid class from a module"""
        # Test loading a built-in class
        result = ClassLoader.load_class('unittest.TestCase')
        self.assertEqual(result, unittest.TestCase)
    
    def test_load_invalid_class(self):
        """Test loading a non-existent class"""
        with self.assertRaises(ClassLoadingError):
            ClassLoader.load_class('nonexistent.module.NonExistentClass')
    
    def test_instantiate_classes(self):
        """Test instantiating multiple classes"""
        with patch.object(ClassLoader, 'load_class') as mock_load:
            mock_class = MagicMock()
            mock_load.return_value = mock_class
            
            instances = ClassLoader.instantiate_classes([
                'module.Class1',
                'module.Class2'
            ])
            
            self.assertEqual(len(instances), 2)
            self.assertEqual(mock_load.call_count, 2)
            mock_class.assert_called()


class TestAgentFactory(unittest.TestCase):
    def setUp(self):
        # Clear the registry before each test
        AgentFactory._registry = {}
    
    def test_register_agent(self):
        """Test registering an agent class"""
        AgentFactory.register_agent('test', FinanceAgent)
        self.assertIn('test', AgentFactory._registry)
        self.assertEqual(AgentFactory._registry['test'], FinanceAgent)
    
    def test_register_invalid_agent(self):
        """Test registering a non-agent class"""
        class NotAnAgent:
            pass
            
        with self.assertRaises(ValueError):
            AgentFactory.register_agent('invalid', NotAnAgent)
    
    def test_create_agent(self):
        """Test creating an agent instance"""
        AgentFactory.register_agent('test', FinanceAgent)
        config = {'model': 'test-model', 'prompt': 'test-prompt', 'tools': []}
        agent = AgentFactory.create('test', config)
        self.assertIsInstance(agent, FinanceAgent)
    
    def test_create_unregistered_agent(self):
        """Test creating an unregistered agent"""
        with self.assertRaises(ValueError):
            AgentFactory.create('nonexistent', {})


class TestAgentConfiguration(TestCase):
    def setUp(self):
        from finance_bot.langchain_bot.models import AgentSettings
        self.settings = AgentSettings.objects.create(
            model='test-model',
            prompt='test-prompt',
            is_default=True
        )
    
    def test_get_agent_settings(self):
        """Test getting agent settings"""
        settings = AgentConfiguration.get_agent_settings('test-user')
        self.assertEqual(settings.model, 'test-model')
        self.assertEqual(settings.prompt, 'test-prompt')
    
    def test_get_agent_config(self):
        """Test getting complete agent configuration"""
        config = AgentConfiguration.get_agent_config('test-user')
        self.assertEqual(config['model'], 'test-model')
        self.assertEqual(config['prompt'], 'test-prompt')
        self.assertIn('tools', config)
        self.assertIn('use_memory', config)


class TestFinanceAgent(TestCase):
    def setUp(self):
        from finance_bot.langchain_bot.models import AgentSettings
        self.settings = AgentSettings.objects.create(
            model='test-model',
            prompt='test-prompt {user_name}',
            is_default=True
        )
        
        # Register the agent with the factory
        AgentFactory.register_agent('finance', FinanceAgent)
    
    @patch('finance_bot.agents.finance_agent.ChatOpenAI')
    @patch('finance_bot.agents.finance_agent.create_react_agent')
    def test_agent_initialization(self, mock_create_agent, mock_chat_openai):
        """Test finance agent initialization"""
        # Mock the agent creation
        mock_agent = MagicMock()
        mock_create_agent.return_value = mock_agent
        
        # Create agent with test config
        config = {
            'model': 'test-model',
            'prompt': 'test-prompt',
            'tools': [],
            'use_memory': True
        }
        
        agent = FinanceAgent(config)
        
        # Verify the agent was created with the correct parameters
        mock_chat_openai.assert_called_once_with(
            model='test-model',
            api_key=os.getenv('OPENAI_API_KEY')
        )
        mock_create_agent.assert_called_once()
        
        # Test agent invocation
        context = {
            'user_id': 'test-user',
            'user_name': 'Test User',
            'input': 'Hello, world!'
        }
        
        # Mock the agent's invoke method
        mock_agent.invoke.return_value = {'messages': [MagicMock(content='Test response')]}
        
        response = agent.invoke(context)
        self.assertEqual(response, 'Test response')
