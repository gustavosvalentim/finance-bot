from django.core.management import BaseCommand
from finance_bot.agents.crew import crew


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        """
        This command runs the Crew AI agents for price research and comparison.
        """

        while True:
            try:
                prompt = input(">> ")
                result = crew.kickoff(inputs={'user': '51994709234', 'prompt': prompt})
                print(result)
            except KeyboardInterrupt:
                print("Exiting the crew...")
                exit()
            except:
                print("An error occurred. Stopping crew.")
                exit()
