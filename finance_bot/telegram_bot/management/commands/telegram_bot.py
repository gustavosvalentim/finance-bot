import os
import telebot

from django.core.management import BaseCommand

from finance_bot.agents.factory import AgentFactory
from finance_bot.agents.config import AgentConfiguration
from finance_bot.logging import get_logger
from finance_bot.telegram_bot import middlewares
from finance_bot.telegram_bot.models import TelegramUserSettings
from finance_bot.finance.constants import FINANCE_AGENT_NAME

TELEGRAM_API_KEY = os.environ.get("TELEGRAM_API_KEY")

bot = telebot.TeleBot(TELEGRAM_API_KEY)

middleware_manager = middlewares.MiddlewareManager()
middleware_manager.register(middlewares.RateLimitMiddleware(bot))
middleware_manager.register(middlewares.UserInteractionMiddleware(bot))


@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    config = AgentConfiguration.get_agent_config(user_id=str(message.from_user.id))
    agent = AgentFactory.create(FINANCE_AGENT_NAME, config)

    can_continue = middleware_manager.execute(message.chat.id, message.from_user.id, message.text)
    if not can_continue:
        return

    telegram_user_settings = TelegramUserSettings.objects.filter(telegram_id=message.from_user.id).first()
    if telegram_user_settings is None:
        bot.send_message(message.chat.id, "Please setup your account first.")
        return

    response = agent.invoke({
        'user_id': str(message.from_user.id),
        'user_name': message.from_user.first_name,
        'input': message.text
    })
    
    bot.send_message(message.chat.id, response)


class Command(BaseCommand):
    help = "Telegram bot"

    def handle(self, *args, **kwargs):
        logger = get_logger("MrBuffet Bot")

        try:
            logger.info("Mr Buffet says hi.")
            logger.info("Listening for messages.")

            bot.infinity_polling()
        except:
            logger.info("Mr Buffet says bye.")
            bot.stop_bot()
            exit()
