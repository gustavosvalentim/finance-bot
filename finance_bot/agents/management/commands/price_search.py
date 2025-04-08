import os

from crewai import Crew, Agent, Task
from crewai.tools import tool
from crewai_tools import ScrapeWebsiteTool
from django.core.management.base import BaseCommand
from googlesearch import search
from langchain_openai import ChatOpenAI


os.environ['OPENAI_API_KEY'] = '1234567890'  # This is not needed for ollama
                                             # but it's required for ChatOpenAI or other models

llm = ChatOpenAI(model="ollama/llama3.3", base_url="http://localhost:11434")
verbose = True


scrape_website_tool = ScrapeWebsiteTool()


@tool
def google_search_tool(query: str) -> str:
    """
    Perform a Google search and return the first result.
    """

    results = search(query, num_results=25, advanced=True)
    output = ""

    for item in results:
        output += f"Title: {item.title}\n"
        output += f"URL: {item.url}\n"
        output += "-" * 20 + "\n\n"

    return output


class Command(BaseCommand):
    help = "Runs the Price Research and Comparison Crew"

    def handle(self, *args, **options):
        scraper_agent = Agent(
            role="E-commerce Price Scraper",
            goal="Scrape prices and availability of a specific product from various e-commerce websites.",
            tools=[google_search_tool, scrape_website_tool],
            verbose=verbose,
            backstory="""
                The E-commerce Price Scraper agent is designed to gather accurate and up-to-date pricing information from multiple e-commerce platforms.
                It ensures that users have access to detailed product availability and pricing data, enabling them to make informed purchasing decisions.
                This agent is the first step in identifying the best deals for any product online.
            """,
            llm=llm,
        )
        comparison_agent = Agent(
            role="Price Comparison and Conversion Specialist",
            goal=(
                "Compare scraped prices, convert them to the specified country's currency, "
                "and identify the e-commerce website offering the lowest price for the product."
            ),
            tools=[google_search_tool, scrape_website_tool],  # Add any currency conversion tools here if needed
            verbose=verbose,
            allow_delegation=True,
            backstory="""
                The Price Comparison and Conversion Specialist agent takes the pricing data collected by the scraper and analyzes it to find the best deal.
                It converts all prices into the user's specified local currency and identifies the website offering the lowest price.
                This agent ensures that users always get the best value for their purchases, tailored to their location.
            """,
            llm=llm,
        )
        scrape_task = Task(
            description="Scrape prices and availability for {product} from various e-commerce websites.",
            expected_output="A list of prices and availability for the product from different e-commerce websites.",
            human_input=False,
            agent=scraper_agent,
        )
        compare_and_convert_task = Task(
            description=(
                "Compare the scraped prices for {product}, convert them to {country}'s currency, "
                "and identify the website offering the lowest price."
            ),
            expected_output="The e-commerce website with the lowest price for the product, adjusted to the specified country's currency.",
            human_input=True,
            agent=comparison_agent,
        )
        price_search_crew = Crew(
            agents=[scraper_agent, comparison_agent],
            tasks=[scrape_task, compare_and_convert_task],
            verbose=verbose,
        )

        inputs = {
            "product": "Samsung Galaxy S23 Ultra",
            "country": "Brazil",
        }

        print(price_search_crew.kickoff(inputs=inputs))
