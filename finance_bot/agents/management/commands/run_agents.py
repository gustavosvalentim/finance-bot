from django.core.management.base import BaseCommand

from finance_bot.agents.crew import FinanceManagementCrew


class Command(BaseCommand):
    help = "Runs the Crew of agents"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting the Crew of agents..."))
        crew = FinanceManagementCrew()
        while True:
            try:
                prompt = input(">> ")
                result = crew.kickoff(inputs={"prompt": prompt})
                print(result)
            except KeyboardInterrupt:
                self.stdout.write(self.style.WARNING("Stopping the Crew of agents..."))
                break

        self.stdout.write(self.style.SUCCESS("Crew of agents finished."))
