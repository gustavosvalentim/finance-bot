import os

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

                output = agent.invoke(os.environ.get("USER_ID"), os.environ.get("USER_NICKNAME"), user_input)

                for message in output["messages"]:
                    logger.debug(message)    
                
                print(f"Agent: {output['messages'][-1].content}")
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as err:
                logger.error("An error ocurred. Please try again. %s.", err, exc_info=True)
                continue
