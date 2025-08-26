import json
import logging

from channels.generic.websocket import WebsocketConsumer

from finance_bot.finance.agent import FinanceAgent


logger = logging.getLogger(__name__)


class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.agent = None

    def connect(self):
        try:
            logger.info(f"User {self.scope['user']} connected")
            self.agent = FinanceAgent()
            self.accept()
        except Exception as e:
            logger.error(f"Error connecting user {self.scope['user']}: {e}")
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
            logger.error(f"Error processing message {message} from user {self.scope['user']}: {e}")
            self.send(text_data=json.dumps({
                "message": "There was an error processing your request"
            }))
