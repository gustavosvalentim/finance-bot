import os

from langchain.agents import AgentExecutor
from langchain_openai.chat_models import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.utils import trim_messages
from langchain_core.prompt_values import ChatPromptValue
from langchain_core.runnables import RunnableConfig

from .base import BaseAgent, AgentError

def _count_tokens(messages: list) -> int:
    """Approximate token counting for message trimming"""
    # This is a simplified token counter. For production, use a real tokenizer.
    return sum(len(str(m.content)) for m in messages)

def pre_model_hook(state: dict, config: RunnableConfig) -> dict:
    """Hook to trim messages before LLM processing"""
    if not isinstance(state, dict) or "messages" not in state:
        return state

    trimmed_messages = trim_messages(
        state["messages"],
        max_tokens=4000,
        strategy="last",
        token_counter=_count_tokens,
        start_on="human",
        allow_partial=False,
        include_system=True,
    )
    
    # Create a new ChatPromptValue with the trimmed messages
    prompt = ChatPromptValue(messages=trimmed_messages)
    
    # Return a dictionary with the expected structure for the next step
    return {"messages": prompt.to_messages()}  # Or however the next component expects it

class FinanceAgent(BaseAgent):
    """Finance-specific agent implementation"""
    
    def _create_agent_executor(self) -> AgentExecutor:
        """Create LangChain agent executor for finance operations"""
        try:
            # Create language model
            model = ChatOpenAI(
                model=self.config.get('model', 'gpt-4o-mini'),
                api_key=os.getenv("OPENAI_API_KEY")
            )
            
            # Configure executor parameters
            executor_params = {
                'model': model,
                'tools': self.tools,
            }
            
            # Add memory if configured
            if self.config.get('use_memory', False):
                executor_params['checkpointer'] = MemorySaver()
            
            # Create the agent with the pre_model_hook
            agent = create_react_agent(**executor_params)
            return agent.with_hooks(pre_model_hook=pre_model_hook)
            
        except Exception as e:
            raise AgentError(f"Failed to create finance agent executor: {e}")
