from django.contrib.auth.models import User
from rest_framework import authentication

from finance_bot.settings import API_KEY


class ApiKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        api_key = request.META.get("HTTP_X_API_KEY")
        if not api_key or api_key != API_KEY:
            return None

        user = User.objects.get_or_create(username="api_user")[0]

        return (user, None)
