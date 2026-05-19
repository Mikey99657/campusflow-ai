from typing import Annotated, TypedDict
from langgraph.graph import add_messages
from langchain_core.messages import AnyMessage


class AgentState(TypedDict):
    """Shared state for all agents in the supervisor graph.

    This state flows between nodes and defines what data each agent can access.
    """
    messages: Annotated[list[AnyMessage], add_messages]
    next_agent: str
    task_type: str
    context_summary: str
    metadata: dict
