import logging
import os
import telebot

from django.core.management import BaseCommand

from finance_bot.finance.agent import FinanceAgent
from finance_bot.telegram_bot.models import TelegramUserSettings
from finance_bot.users.models import UserInteraction
from telegram_bot.handlers import (
    finish_registration,
    is_pending_registration,
    start_registration,
)


TELEGRAM_API_KEY = os.environ.get("TELEGRAM_API_KEY")

bot = telebot.TeleBot(TELEGRAM_API_KEY)
agent = FinanceAgent()


def rate_limit_exceeded(user_id: str) -> bool:
    user_settings = TelegramUserSettings.objects.filter(telegram_id=user_id).first()
    if not user_settings.rate_limit_enabled:
        return False
    
    message_count = UserInteraction.objects.filter(
        user=user_settings.user,
        interaction_type=UserInteraction.InteractionType.MESSAGE,
        # Assuming you want a time frame validation
        # created_at__gte=timezone.now() - timedelta(seconds=self.time_frame),
    ).count()
    if message_count >= user_settings.rate_limit:
        return True
    return False


def save_interaction(user_id: str, message: str, response: str):
    user_settings = TelegramUserSettings.objects.filter(telegram_id=user_id).first()
    if not user_settings:
        return

    user_interaction = UserInteraction.objects.create(
        user=user_settings.user,
        source="telegram",
        interaction_type=UserInteraction.InteractionType.MESSAGE,
        interaction_data=message,
    )

    # This is the answer from the AI
    UserInteraction.objects.create(
        user=user_settings.user,
        source="telegram",
        interaction_type=UserInteraction.InteractionType.RESPONSE,
        interaction_data=response,
        parent=user_interaction,
    )


@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    user_id = message.from_user.id

    if rate_limit_exceeded(user_id):
        bot.send_message(
            message.chat.id,
            "Você atingiu o limit de mensagens permitidas. Tente novamente mais tarde.",
        )
        return
    
    is_user_configured = TelegramUserSettings.objects.filter(telegram_id=user_id).exists()

    if not is_user_configured and message == '/register':
        response = start_registration(str(user_id))
        bot.send_message(message.chat.id, response)
        return
    
    if is_pending_registration(user_id):
        response = finish_registration(str(user_id), message.text)
        bot.send_message(message.chat.id, response)
        return

    if not is_user_configured:
        bot.send_message(message.chat.id, "Por favor, configure sua conta primeiro.")
        return

    response = agent.invoke({
        'user_id': str(user_id),
        'message': message.text,
    })

    bot.send_message(message.chat.id, response)
    save_interaction(user_id, message.text, response)


class Command(BaseCommand):
    help = "Telegram bot"

    def handle(self, *args, **kwargs):
        logger = logging.getLogger("MrBuffet Bot")

        try:
            logger.info("Mr Buffet says hi.")
            logger.info("Listening for messages.")

            bot.infinity_polling()
        except:
            logger.info("Mr Buffet says bye.")
            bot.stop_bot()
            exit()
