import os
import telebot

from django.core.management import BaseCommand
from finance_bot.logging import get_logger
from finance_bot.langchain_bot.agent import FinanceAgent
from finance_bot.telegram_bot import middlewares


TELEGRAM_API_KEY = os.environ.get("TELEGRAM_API_KEY")

bot = telebot.TeleBot(TELEGRAM_API_KEY)

middleware_manager = middlewares.MiddlewareManager()
middleware_manager.register(middlewares.RateLimitMiddleware(bot))
middleware_manager.register(middlewares.UserInteractionMiddleware(bot))

agent = FinanceAgent()


@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    can_continue = middleware_manager.execute(message.from_user.id, message.text)
    if not can_continue:
        return

    response = agent.invoke(message.from_user.id, message.from_user.first_name, message.text)
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
