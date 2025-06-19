from django.db import models

from finance_bot.users.models import User


class AgentSettingsManager(models.Manager):

    def create(self, *args, **kwargs):
        if kwargs.get("is_default", False) and self.filter(is_default=True).exists():
            raise ValueError("Can't have more than one default agent settings")
        super().create(*args, **kwargs)


class AgentSettings(models.Model):
    prompt = models.TextField()
    model = models.CharField(max_length=100, default="gpt-4o-mini")
    is_default = models.BooleanField(default=False)

    objects = AgentSettingsManager

    class Meta:
        verbose_name_plural = 'Agent settings'

    def __str__(self):
        suffix = " (default)" if self.is_default else ""
        return ' '.join(self.model, suffix)


class AgentSettingsToUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    agent_settings = models.ForeignKey(AgentSettings, on_delete=models.CASCADE)
