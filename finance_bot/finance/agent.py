from datetime import datetime
from logging import config
import os
from typing import Any, Dict

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, trim_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationTokenBufferMemory
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

from finance_bot.finance import tools
from finance_bot.langchain_bot.models import AgentSettings, AgentSettingsToUser
from finance_bot.users.models import User


trimmer = trim_messages(strategy="last", max_tokens=2, token_counter=len)


class FinanceAgent:
    required_keys = ['user_id', 'user_name']
    memory = MemorySaver()

    def _get_agent_configuration(self, user_id: str) -> Dict[str, Any]:
        user_config = AgentSettingsToUser.objects.filter(user__pk=user_id).first()
        agent_config = user_config.agent_settings if user_config else None

        if not agent_config:
            agent_config = AgentSettings.objects.filter(is_default=True).first()

        # user = User.objects.filter(id=user_id).first()
        # system_prompt = agent_config.prompt \
        #     .replace('{user_id}', str(user.pk)) \
        #     .replace('{user_name}', user.first_name) \
        #     .replace('{now}', datetime.now().isoformat())

        # prompt_template = f"""
        # This is a conversation between an human and a bot:
        # {{chat_history}}

        # {system_prompt}

        # The user is asking for: {{input}}
        # """

        # prompt = PromptTemplate(input_variables=['chat_history', 'input'], template=prompt_template)

        prompt = ChatPromptTemplate.from_messages([
            ('system', "Você é um assistente de finanças pessoais. O nome do usuário é {user_name}, e o ID do usuário é {user_id}."),
        ])

        return {
            'model': agent_config.model,
            'prompt': prompt,
        }

    def _get_agent(self, agent_configuration: Dict[str, Any]):
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
        memory = ConversationTokenBufferMemory(memory_key="chat_history", max_token_limit=40000)
        model = ChatOpenAI(model=agent_configuration['model'], api_key=os.getenv("OPENAI_API_KEY"))
        agent = create_react_agent(model, tools, agent_configuration['prompt'])

        return AgentExecutor(agent=agent, tools=agent_tools, memory=memory, verbose=True)

    def invoke(self, input_value: Dict[str, Any]) -> Dict[str, Any]:
        missing_keys = [key for key in self.required_keys if key not in input_value]
        if missing_keys:
            raise ValueError(f"Missing required keys: {', '.join(missing_keys)}")

        agent_config = self._get_agent_configuration(input_value['user_id'])
        agent = self._get_agent(agent_config)
        invoke_config = {
            'configurable': {
                'user_id': input_value['user_id'],
            }
        }

        response = agent.invoke(
            input=input_value,
            config=invoke_config
        )

        return response['messages'][-1].content
    
    def _call_model_wrapper(self, input_value: Dict[str, Any]):
        config = self._get_agent_configuration(input_value['user_id'])
        system_prompt = config['prompt'].invoke(input_value)
        model = ChatOpenAI(model=config['model'], api_key=os.getenv("OPENAI_API_KEY"))
        def call_model(state: MessagesState):
            trimmed_messages = trimmer.invoke(state['messages'])
            messages = system_prompt.to_messages() + trimmed_messages
            response = model.invoke(messages)
            return {'messages': response}
        return call_model

    def invoke_workflow(self, input_value: Dict[str, Any]) -> str:
        workflow = StateGraph(state_schema=MessagesState)
        workflow.add_node("model", self._call_model_wrapper(input_value))
        workflow.add_edge(START, "model")

        app = workflow.compile(checkpointer=self.memory)

        try:
            response = app.invoke(
                {
                    'messages': [HumanMessage(content=input_value['input'])],
                },
                config={'configurable': {'thread_id': input_value['user_id']}},
           )
        except Exception as e:
            print(f"Error invoking workflow: {e}")
            return

        return response['messages'][-1].content
