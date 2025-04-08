import json

from django.core.management.base import BaseCommand

from finance_bot.agents import crew 


class Command(BaseCommand):
    help = "Runs the Crew of agents"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting the Crew of agents..."))
        orchestration_crew = crew.OrchestrationCrew()
        finance_manager_crew = crew.FinanceManagementCrew()
        price_research_crew = crew.PriceResearchCrew()
        while True:
            try:
                prompt = input(">> ")
                result = orchestration_crew.crew().kickoff(inputs={"prompt": prompt})
                json_output = json.loads(result.json)

                if json_output['agent_name'] == 'finances_manager':
                    finance_result = finance_manager_crew.crew().kickoff(inputs=json_output)
                    print(finance_result.json)
                # elif json_output['agent_name'] == 'price_researcher':
                #     price_research_result = price_research_crew.crew().kickoff(inputs=json_output)
                #     print(price_research_result.json)
            except KeyboardInterrupt:
                self.stdout.write(self.style.WARNING("Stopping the Crew of agents..."))
                break

        self.stdout.write(self.style.SUCCESS("Crew of agents finished."))
