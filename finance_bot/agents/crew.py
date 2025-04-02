import os

from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, task, crew
from langchain_openai import ChatOpenAI


os.environ["OPENAI_API_KEY"] = "1234567890"  # This is not needed for ollama
                                             # but it's required for ChatOpenAI or other models


@CrewBase
class FinanceManagementCrew:
    """Crew of agents for finance management and organization."""

    llm = ChatOpenAI(model="ollama/llama3.1", base_url="http://localhost:11434")

    # Paths to YAML configuration files
    agents_config = 'config/agents.yml'
    tasks_config = 'config/tasks.yml'

    @agent
    def transactions(self) -> Agent:
        """Agent for managing transactions."""

        return Agent(
            config=self.agents_config['transactions'],
            llm=self.llm,
        )
    
    @task
    def transactions_task(self) -> Task:
        """Task for managing transactions."""

        return Task(
            config=self.tasks_config['transactions_task'],
            llm=self.llm,
        )
    
    @crew
    def crew(self) -> Crew:
        """Crew of agents for finance management."""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
        )

    def kickoff(self, inputs: dict) -> str:
        """Kickoff the crew with the given inputs."""

        # Run the crew and get the result
        return self.crew().kickoff(inputs)
