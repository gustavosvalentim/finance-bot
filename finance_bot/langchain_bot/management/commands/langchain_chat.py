import logging
from django.core.management import BaseCommand
from finance_bot.langchain_bot.agent import FinanceAgent
from finance_bot.langchain_bot.logging import get_logger


class Command(BaseCommand):
    help = "Runs the Langchain Chat Agent"

    def handle(self, *args, **options):
        logger = get_logger('LangchainChatAgent')
        agent = FinanceAgent()

        while True:
            try:
                user_input = input("You: ")

                if user_input.lower() == "bye":
                    self.stdout.write("\nExiting...")
                    break

                output = agent.invoke(user_input)

                for message in output["messages"]:
                    if message.role == "user":
                        logger.debug(f"You: {message.content}")
                    elif message.role == "assistant":
                        logger.debug(f"Agent: {message.content}")
                    else:
                        logger.warning(f"Unknown role: {message.role}")
                
                print(f"Agent: {output['messages'][-1].content}")
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as err:
                logger.error("An error ocurred. Please try again. %s.", err, exc_info=True)
                continue
