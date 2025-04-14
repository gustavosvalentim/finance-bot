import os

from crewai import Crew, Agent, Task
from langchain_openai import ChatOpenAI

from .tools.search_category_tool import SearchCategoryTool
from .tools.search_user_categories_tool import SearchUserCategoriesTool
from .tools.create_category_tool import CreateCategoryTool
from .tools.create_transaction_tool import CreateTransactionTool


# LLM configuration
# This is needed for ChatOpenAI
# Even though it won't be used for ollama
os.environ['OPENAI_API_KEY'] = 'api-pj-123'

llm = ChatOpenAI(model="ollama/llama3.3", base_url="http://localhost:11434")

# Agent configuration
verbose = True

# tools
search_category_tool = SearchCategoryTool() # search by category name
search_user_categories_tool = SearchUserCategoriesTool()
create_category_tool = CreateCategoryTool()
create_transaction_tool = CreateTransactionTool()

transactions_agent = Agent(
    role="Finance Management Agent",
    goal="Manage and organize financial transactions.",
    verbose=verbose,
    tools=[search_category_tool, search_user_categories_tool, create_category_tool, create_transaction_tool],
    backstory="""
        The Finance Management Agent is designed to assist users in managing their financial transactions.
        It can help categorize expenses, track income, and provide insights into spending habits.
    """,
    llm=llm,
)

transactions_task = Task(
    description="Organize and categorize financial transactions.",
    expected_output="""
        Process the user input {prompt}.

        The user identification is {user}.

        If the user is trying to create a transaction, the agent should follow the steps below:
            1. Search for the category of the transaction using the SearchCategoryTool.
            2. If the category was not found, the agent should create a new category using the CreateCategoryTool.
            3. Create the transaction using the CreateTransactionTool, using the Category ID as category instead of the name.
            4. Output a message saying that the transaction was created successfully, including the transaction description and ID.

        If the user is trying to create a category, the agent should follow the steps below:
            1. Search for the category in the database using the SearchCategoryTool.
            2. If the category was not found, create the category using the CreateCategoryTool.

        If the user wants to list all his categories, the agent should follow the steps below:
            1. Search for the categories in the database using the SearchUserCategoriesTool.
            2. Output a list with all the categories found.
            3. If no categories were found, output a message saying that no categories were found.

        Observations:
            - If the user wants to list his categories, don't create anything, only list the categories.
            - After you use the SearchUserCategoriesTool, output the result to the user and stop the task.
            - Try to match the category name even if the user misspells it.
    """,
    agent=transactions_agent,
)

crew = Crew(
    name="Finance Management Crew",
    agents=[transactions_agent],
    tasks=[transactions_task],
    memory=True,
    verbose=verbose,
)
