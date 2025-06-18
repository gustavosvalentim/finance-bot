import json

from channels.generic.websocket import WebsocketConsumer
from finance_bot.langchain_bot.agent import FinanceAgent


class ChatConsumer(WebsocketConsumer):
    connections = {}
    agent = FinanceAgent()

    def connect(self):
        self.connections.update({
            self.scope['user'].id: self.channel_name,
        })
        self.accept()

    def disconnect(self, close_code):
        for user_id in self.connections.keys():
            if self.scope['user'].id == user_id:
                self.connections.pop(user_id)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        response = self.agent.invoke(self.scope['user'].id, self.scope['user'].first_name, message)

        self.send(text_data=json.dumps({"message": response['messages'][-1].content}))
