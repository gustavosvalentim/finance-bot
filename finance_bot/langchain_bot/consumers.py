import json

from channels.generic.websocket import WebsocketConsumer
from finance_bot.langchain_bot.agent import FinanceAgent


class ChatConsumer(WebsocketConsumer):
    connections = {}
    agent = FinanceAgent()

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        response = self.agent.invoke(self.scope['user'].id, self.scope['user'].first_name, message)

        self.send(text_data=json.dumps({"message": response}))
