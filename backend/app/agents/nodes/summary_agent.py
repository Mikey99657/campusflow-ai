from langchain_core.messages import SystemMessage, AIMessage

from app.agents.prompts.loader import load_prompt
from app.core.llm_factory import create_llm


def build_summary_agent():
    """Build the summary agent as a simple LLM call node."""
    llm = create_llm()
    system_prompt = load_prompt("summary_system")

    def summary_agent_node(state):
        messages = [SystemMessage(content=system_prompt)] + state["messages"]
        response = llm.invoke(messages)
        return {"messages": [AIMessage(content=response.content, name="summary_agent")]}

    return summary_agent_node
