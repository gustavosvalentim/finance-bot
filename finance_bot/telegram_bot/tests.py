from django.test import TestCase
from finance_bot.telegram_bot.middlewares import RateLimitMiddleware, UserInteractionMiddleware
from finance_bot.telegram_bot.models import TelegramUserSettings
from finance_bot.users.models import User, UserInteraction


class FakeTeleBot:
    """
    A fake TeleBot class for testing purposes.
    """
    def __init__(self):
        self.users = {}

    def send_message(self, *args, **kwargs):
        pass


class TelegramBotTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create(
            email="test@test.com",
            telegram_id="123456789",
        )
        self.telegram_user_settings = TelegramUserSettings.objects.create(
            telegram_id="123456789",
            rate_limit_enabled=True,
            rate_limit=5
        )

        for i in range(5):
            UserInteraction.objects.create(
                user=self.user,
                source="test_source",
                interaction_type=UserInteraction.InteractionType.MESSAGE,
                interaction_data=f"Test interaction {i}"
            )

    def test_rate_limit_middleware(self):
        # Create an instance of the RateLimitMiddleware
        rate_limit_middleware = RateLimitMiddleware(FakeTeleBot())

        can_send_message = rate_limit_middleware.handle(self.user.telegram_id, "Test message")
        self.assertFalse(can_send_message, "User should not be able to send more messages than the limit.")

    def test_user_interaction_middleware(self):
        # Create an instance of the UserInteractionMiddleware
        initial_count = UserInteraction.objects.filter(user=self.user).count()
        user_interaction_middleware = UserInteractionMiddleware(FakeTeleBot())

        can_send_message = user_interaction_middleware.handle(self.user.telegram_id, "Test message")
        self.assertTrue(can_send_message, "User should be able to send a message.")
        self.assertEqual(
            UserInteraction.objects.filter(user=self.user).count(),
            initial_count + 1,
            "User interaction count should increase by 1."
        )
