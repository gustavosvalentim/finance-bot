from django.db import models

from finance_bot.users.models import User


class AgentSettings(models.Model):
    prompt = models.TextField()
    model = models.CharField(max_length=100, default="gpt-4o-mini")
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Agent settings'

    def save(self, *args, **kwargs):
        if self.is_default and self.objects.filter(is_default=True).exists():
            raise ValueError('Cannot have more than one default agent settings')
        return super().save(*args, **kwargs)


class AgentSettingsToUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    agent_settings = models.ForeignKey(AgentSettings, on_delete=models.CASCADE)
