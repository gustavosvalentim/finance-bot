from abc import ABC, abstractmethod
from telebot import TeleBot
from finance_bot.users.models import UserInteraction
from finance_bot.telegram_bot.models import TelegramUserSettings


class Middleware(ABC):
    """
    Base middleware class.
    """

    def __init__(self, bot: TeleBot):
        self.bot = bot

    @abstractmethod
    def handle(self, user_id: str, message: str) -> bool:
        """
        Handle the middleware logic.
        """
        raise NotImplementedError("Subclasses must implement this method.")


class MiddlewareManager:
    """
    Middleware manager to run middlewares.
    """

    def __init__(self, middlewares: list[Middleware] = []):
        self.middlewares = middlewares

    def register(self, middleware: Middleware):
        """
        Register a new middleware.
        """

        self.middlewares.append(middleware)
        return self

    def execute(self, user_id: str, message: str) -> bool:
        """
        Run all middlewares.
        """

        for middleware in self.middlewares:
            if not middleware.handle(user_id, message):
                return False

        return True



class RateLimitMiddleware(Middleware):
    """
    Middleware to limit the number of messages a user can send in a given time frame.
    """

    def __init__(self, bot: TeleBot):
        self.bot = bot

    def handle(self, user_id: str, message: str) -> bool:
        """
        Handle the rate limit for a user.
        """
        # This is a placeholder for the actual implementation.
        # In a real-world scenario, you would check the user's message count
        # and the time frame to determine if they are within the limit.
        
        user_settings = TelegramUserSettings.objects.filter(telegram_id=user_id).first()
        if not user_settings.rate_limit_enabled:
            return True
        
        message_count = UserInteraction.objects.filter(
            user=user_settings.user,
            interaction_type=UserInteraction.InteractionType.MESSAGE,
            # Assuming you want a time frame validation
            # created_at__gte=timezone.now() - timedelta(seconds=self.time_frame),
        ).count()
        if message_count >= user_settings.rate_limit:
            self.bot.send_message(
                user_settings.telegram_id,
                "Você atingiu o limit de mensagens permitidas. Tente novamente mais tarde.",
            )
            return False

        return True
    

class UserInteractionMiddleware(Middleware):
    """
    Middleware to log user interactions.
    """

    def __init__(self, bot: TeleBot):
        self.bot = bot

    def handle(self, user_id: str, message: str) -> bool:
        """
        Handle user interaction logging.
        """
        user_settings = TelegramUserSettings.objects.filter(telegram_id=user_id).first() 
        if not user_settings:
            return False

        UserInteraction.objects.create(
            user=user_settings.user,
            source="telegram",
            interaction_type=UserInteraction.InteractionType.MESSAGE,
            interaction_data=message,
        )

        return True
