from django.apps import AppConfig


class LangchainBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'finance_bot.langchain_bot'

    def ready(self):
        from django.db import connection
        from finance_bot.langchain_bot.models import AgentSettings

        tables = connection.introspection.table_names()

        if not AgentSettings._meta.db_table in tables:
            return

        if not AgentSettings.objects.filter(is_default=True).exists():
            with open("conf/prompt.txt", "r", encoding="utf-8") as prompt_buf:
                prompt = prompt_buf.read()
                AgentSettings.objects.create(
                    prompt=prompt,
                    is_default=True,
                )
