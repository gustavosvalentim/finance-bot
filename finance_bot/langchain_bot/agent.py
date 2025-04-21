import os

from datetime import datetime

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# import tools
from finance_bot.langchain_bot.tools import (
    CreateCategoryTool,
    CreateTransactionTool,
    SearchUserCategoriesTool,
    SearchCategoryTool,
    SearchTransactionsTool,
)


class FinanceAgent:
    memory = MemorySaver()
    model = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"], model="gpt-4o-mini")
    tools = [
        CreateCategoryTool(),
        CreateTransactionTool(),
        SearchUserCategoriesTool(),
        SearchCategoryTool(),
        SearchTransactionsTool(),
    ]
    agent_executor = create_react_agent(model, tools, checkpointer=memory)
    default_config = {
        'configurable': {
            'thread_id': '1234567890',
        }
    }
    system_prompt = """
        The user identification is {user_id}.

        Now is {now}.

        If the user is trying to create a transaction, the agent should follow the steps below:
            1. Search for the category of the transaction using the SearchCategoryTool, using the `user identification` as filter.
            2. If the category was not found, the agent should create a new category using the CreateCategoryTool.
            3. Create the transaction using the CreateTransactionTool, using the Category ID as category instead of the name.
            4. Output a message saying that the transaction was created successfully, including its details.

        If the user is trying to create a category, the agent should follow the steps below:
            1. Search for the category in the database using the SearchCategoryTool.
            2. If the category was not found, create the category using the CreateCategoryTool.

        If the user wants to list all his categories, the agent should follow the steps below:
            1. Search for the categories in the database using the SearchUserCategoriesTool.
            2. Output a list with all the categories found.
            3. If no categories were found, output a message saying that no categories were found.
                                
        If the user wants to list his transactions, the agent should follow the steps below:
            1. Determine what is the date range the user wants to see the transactions, if the user doesn't specify the start_date should be 30 days before now and end_date should be now.
            2. Search for the transactions in the database using the SearchTransactionsTool.
            3. Output a list with all the transactions found.
            4. If no transactions were found, output a message saying that no transactions were found.

        Observations:
            - If the user wants to list his categories, don't create anything, only list the categories.
            - After you use the SearchUserCategoriesTool, output the result to the user and stop the task.
            - Try to match the category name even if the user misspells it.
            - When creating a trasaction, if the user specifies a date use it instead of the current date in YYYY-MM-DD format."""

    def invoke(self, query: str) -> str:
        """Invoke the agent with the given query."""

        system_prompt_formatted = self.system_prompt.format(
            user_id=os.environ["USER_ID"],
            now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        return self.agent_executor.invoke(
            {'messages': [SystemMessage(content=system_prompt_formatted), HumanMessage(content=query)]},
            config=self.default_config,
        )
