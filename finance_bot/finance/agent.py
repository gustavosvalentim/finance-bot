import os
from datetime import datetime
from typing import Any, Dict

from langchain_openai import ChatOpenAI
from langchain_core.messages.utils import trim_messages, count_tokens_approximately
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from finance_bot.finance import tools
from finance_bot.langchain_bot.models import AgentSettings, AgentSettingsToUser
from finance_bot.users.models import User


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
        user_config = AgentSettingsToUser.objects.filter(user__pk=user_id).first()
        agent_config = user_config.agent_settings if user_config else None

        if not agent_config:
            agent_config = AgentSettings.objects.filter(is_default=True).first()

        user = User.objects.filter(pk=user_id).first()
        prompt = agent_config.prompt.format(user_name=user.first_name, user_id=user.pk, now=datetime.now().isoformat())

        return {
            'model': agent_config.model,
            'prompt': prompt,
        }

    def _get_agent(self, agent_configuration: Dict[str, Any]):
        model = ChatOpenAI(model=agent_configuration['model'], api_key=os.getenv("OPENAI_API_KEY"))
        agent = create_react_agent(
            model,
            self.agent_tools,
            prompt=agent_configuration['prompt'],
            checkpointer=self.memory,
            pre_model_hook=pre_model_hook
        )
        return agent

    def invoke(self, input_value: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke the agent with the given input value.

        Input value is a dict and should contain the following keys:
        - user_id: The ID of the user invoking the agent.
        - input: The input message for the agent.
        """

        agent_config = self._get_agent_configuration(input_value['user_id'])
        agent = self._get_agent(agent_config)
        invoke_config = {
            'configurable': {
                'thread_id': input_value['user_id'],
            }
        }

        response = agent.invoke({'messages': ('human', input_value['input'])}, config=invoke_config)

        return response['messages'][-1].content
