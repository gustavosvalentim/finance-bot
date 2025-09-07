import os
from datetime import datetime
from typing import Any, Dict
from typing_extensions import TypedDict

from langchain_openai import ChatOpenAI
from langchain_core.messages.utils import trim_messages, count_tokens_approximately
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from finance_bot.finance import tools
from finance_bot.langchain_bot.models import AgentSettings
from finance_bot.users.models import User


class AgentInvokeArgs(TypedDict):
    user_id: str
    message: str


def pre_model_hook(state):
    trimmed_messages = trim_messages(
        state["messages"],
        strategy="last",
        token_counter=count_tokens_approximately,
        max_tokens=1000,
        start_on="human",
        end_on=("human", "tool"),
    )
    return {"llm_input_messages": trimmed_messages}


class FinanceAgent:
    memory = MemorySaver()
    agent_tools = [
        tools.CreateCategoryTool(),
        tools.CreateTransactionTool(),
        tools.SearchCategoryByNameTool(),
        tools.SearchUserCategoriesTool(),
        tools.SearchTransactionsTool(),
        tools.UpdateTransactionTool(),
        tools.DeleteTransactionTool(),
        tools.DeleteCategoryTool(),
        tools.UpdateCategoryTool(),
    ]

    def _get_agent_configuration(self, user_id: str) -> Dict[str, Any]:
        user = User.objects.filter(pk=user_id).first()
        agent_config = AgentSettings.objects.find_by_user(user)

        if agent_config is None:
            raise ValueError("No agent configuration found for user.")

        prompt = agent_config.prompt.format(user_name=user.first_name, user_id=user.pk, now=datetime.now().isoformat())

        return {
            'model': agent_config.model,
            'prompt': prompt,
        }

    def _get_agent(self, agent_configuration: Dict[str, Any]):
        model = ChatOpenAI(
            model=agent_configuration['model'],
            api_key=os.getenv("OPENAI_API_KEY"),
            reasoning_effort='minimal',
            temperature=1,
        )
        agent = create_react_agent(
            model,
            self.agent_tools,
            prompt=agent_configuration['prompt'],
            checkpointer=self.memory,
            pre_model_hook=pre_model_hook
        )
        return agent

    def invoke(self, args: AgentInvokeArgs) -> str:
        """Invoke the agent with the given input value.

        Parameters:
            args (AgentInvokeArgs): A dictionary containing 'user_id' and 'message' keys.

        Returns:
            str: The agent response. 
        """

        user_id = args.get('user_id')
        message = args.get('message')

        if user_id is None or user_id.strip() == '':
            raise ValueError("User ID can't be empty.")

        if message is None or message.strip() == '':
            raise ValueError("Message can't be empty.")

        agent_config = self._get_agent_configuration(user_id)
        agent = self._get_agent(agent_config)
        invoke_config = {
            'configurable': {
                'thread_id': user_id,
            }
        }

        response = agent.invoke({'messages': ('human', message)}, config=invoke_config)

        return response['messages'][-1].content
