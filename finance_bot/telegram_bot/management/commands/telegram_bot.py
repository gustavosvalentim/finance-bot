import logging
import os
import telebot

from django.core.management import BaseCommand

from finance_bot.finance.agent import FinanceAgent
from finance_bot.telegram_bot.models import TelegramUserSettings
from finance_bot.users.models import UserInteraction

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
    if rate_limit_exceeded(message.from_user.id):
        bot.send_message(
            message.chat.id,
            "Você atingiu o limit de mensagens permitidas. Tente novamente mais tarde.",
        )

    telegram_user_settings = TelegramUserSettings.objects.filter(telegram_id=message.from_user.id).first()
    if telegram_user_settings is None:
        bot.send_message(message.chat.id, "Por favor, configure sua conta primeiro.")
        return

    response = agent.invoke({
        'user_id': str(message.from_user.id),
        'input': message.text,
    })

    bot.send_message(message.chat.id, response)
    save_interaction(message.from_user.id, message.text, response)


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
