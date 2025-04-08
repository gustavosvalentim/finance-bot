import os

from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import ScrapeWebsiteTool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel


os.environ["OPENAI_API_KEY"] = "1234567890"  # This is not needed for ollama
                                             # but it's required for ChatOpenAI or other models


class OrchestrationOutput(BaseModel):
    """Output model for the orchestration agent."""

    agent_name: str
    prompt: str
    description: str

@CrewBase
class OrchestrationCrew:
    """Crew of agents for finance management and organization."""

    llm = ChatOpenAI(model="ollama/llama3.3", base_url="http://localhost:11434")

    # Paths to YAML configuration files
    agents_config = 'config/orchestrator/agents.yml'
    tasks_config = 'config/orchestrator/tasks.yml'

    @agent
    def orchestrator(self) -> Agent:
        """Orchestrator agent for managing the crew."""

        return Agent(
            config=self.agents_config['orchestrator'],
            llm=self.llm,
        )
    
    @task
    def orchestrator_task(self) -> Task:
        """Task for the orchestrator agent."""

        return Task(
            config=self.tasks_config['orchestration_task'],
            output_json=OrchestrationOutput,
            llm=self.llm,
        )
    
    @crew
    def crew(self) -> Crew:
        """Crew of agents for finance management."""

        return Crew(
            agents=[self.orchestrator()],
            tasks=[self.orchestrator_task()],
            verbose=True,
        )


class FinanceManagementOutput(BaseModel):
    """Output model for the finance management agent."""

    description: str
    amount: float
    time: str
    category: str
    operation: str


@CrewBase
class FinanceManagementCrew:
    """Crew of agents for finance management and organization."""

    llm = ChatOpenAI(model="ollama/llama3.1", base_url="http://localhost:11434")

    agents_config = 'config/finances_manager/agents.yml'
    tasks_config = 'config/finances_manager/tasks.yml'

    @agent
    def finance_manager(self) -> Agent:
        """Finance manager agent for managing finances."""

        return Agent(
            config=self.agents_config['finance_manager'],
            llm=self.llm,
        )

    @task
    def finance_manager_task(self) -> Task:
        """Task for the finance manager agent."""

        return Task(
            config=self.tasks_config['finance_manager_task'],
            output_json=FinanceManagementOutput,
            llm=self.llm,
        )

    @crew
    def crew(self) -> Crew:
        """Crew of agents for finance management."""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
        )


class PriceResearchOutput(BaseModel):
    """Output model for the price research agent."""

    product_name: str
    price: float
    link: str


@CrewBase
class PriceResearchCrew:
    """Crew of agents for price research and analysis."""

    llm = ChatOpenAI(model="ollama/llama3.1", base_url="http://localhost:11434")

    agents_config = 'config/price_researcher/agents.yml'
    tasks_config = 'config/price_researcher/tasks.yml'

    @agent
    def price_researcher(self) -> Agent:
        """Price researcher agent for conducting price research."""

        return Agent(
            config=self.agents_config['price_researcher'],
            llm=self.llm,
            tools=[ScrapeWebsiteTool()],
        )

    @task
    def price_research_task(self) -> Task:
        """Task for the price researcher agent."""

        return Task(
            config=self.tasks_config['price_researcher_task'],
            output_json=PriceResearchOutput,
            llm=self.llm,
        )

    @crew
    def crew(self) -> Crew:
        """Crew of agents for price research."""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
        )
