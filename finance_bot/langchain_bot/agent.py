from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# import tools
from finance_bot.agents.tools import (
    create_category_tool,
    create_transaction_tool,
    search_user_categories_tool,
    search_category_tool,
)


memory = MemorySaver()
model = ChatOllama(model="llama3.3", base_url="http://localhost:11434")
tools = [
    create_category_tool.CreateCategoryTool(),
    create_transaction_tool.CreateTransactionTool(),
    search_user_categories_tool.SearchUserCategoriesTool(),
    search_category_tool.SearchCategoryTool(),
]
agent_executor = create_react_agent(model, tools, checkpoint=memory)
