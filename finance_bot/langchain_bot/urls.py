from django.urls import path

from finance_bot.langchain_bot import consumers
from finance_bot.langchain_bot import views

urlpatterns = [
    path("chat", views.room, name="chat"),
]

websocket_urlpatterns = [
    path("ws/chat", consumers.ChatConsumer.as_asgi()),
]
