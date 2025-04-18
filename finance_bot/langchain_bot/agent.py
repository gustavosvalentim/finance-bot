import os

from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# import tools
from finance_bot.langchain_bot.tools import (
    CreateCategoryTool,
    CreateTransactionTool,
    SearchUserCategoriesTool,
    SearchCategoryTool,
)


memory = MemorySaver()
model = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"], model="gpt-4o-mini")
tools = [
    CreateCategoryTool(),
    CreateTransactionTool(),
    SearchUserCategoriesTool(),
    SearchCategoryTool(),
]
agent_executor = create_react_agent(model, tools, checkpointer=memory)
