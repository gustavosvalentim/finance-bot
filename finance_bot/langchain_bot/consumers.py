import json

from channels.generic.websocket import WebsocketConsumer

from finance_bot.agents.factory import AgentFactory
from finance_bot.agents.config import AgentConfiguration
from finance_bot.finance.apps import FINANCE_AGENT_NAME

class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.agent = None

    def connect(self):
        try:
            # Get user-specific configuration and create agent
            config = AgentConfiguration.get_agent_config(user_id=str(self.scope['user'].id))
            self.agent = AgentFactory.create(FINANCE_AGENT_NAME, config)
            self.accept()
        except Exception as e:
            self.close(code=1011)  # Internal error
            raise

    def disconnect(self, close_code):
        # Clean up any resources if needed
        self.agent = None

    def receive(self, text_data):
        if not self.agent:
            self.send(text_data=json.dumps({
                "message": "Agent not initialized. Please reconnect."
            }))
            return

        try:
            text_data_json = json.loads(text_data)
            message = text_data_json["message"]

            response = self.agent.invoke({
                'user_id': str(self.scope['user'].id),
                'user_name': self.scope['user'].first_name or 'User',
                'input': message
            })

            self.send(text_data=json.dumps({"message": response}))
            
        except json.JSONDecodeError:
            self.send(text_data=json.dumps({
                "message": "Invalid JSON format in message"
            }))
        except Exception as e:
            self.send(text_data=json.dumps({
                "message": f"Error processing your request: {str(e)}"
            }))
