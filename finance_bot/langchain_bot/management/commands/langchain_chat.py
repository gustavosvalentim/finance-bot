from django.core.management import BaseCommand
from langchain_core.messages import HumanMessage
from finance_bot.langchain_bot.agent import FinanceAgent


class Command(BaseCommand):
    help = "Runs the Langchain Chat Agent"

    def handle(self, *args, **options):
        agent = FinanceAgent()
        while True:
            try:
                user_input = input("You: ")

                if user_input.lower() == "bye":
                    print("\nExiting...")
                    break

                output = agent.invoke(user_input)
                
                print(f"Agent: {output['messages'][-1].content}")
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as err:
                print(err)
                print("An error occurred. Please try again.")
                continue
