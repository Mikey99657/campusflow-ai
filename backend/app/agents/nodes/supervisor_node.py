from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage

from app.agents.state import AgentState
from app.agents.prompts.loader import load_prompt
from app.core.llm_factory import create_llm


class RouteDecision(BaseModel):
    """Structured output for supervisor routing decision."""
    next: str = Field(description="Next agent: coding_agent | report_agent | uml_agent | summary_agent | FINISH")
    reason: str = Field(description="Brief reason for routing decision")


def supervisor_node(state: AgentState) -> dict:
    """Supervisor node: routes requests to specialist agents.

    Uses LLM with structured output to decide which agent should handle
    the current task.
    """
    llm = create_llm(temperature=0)

    # Load supervisor prompt
    system_prompt = load_prompt(
        "supervisor_system",
        context_summary=state.get("context_summary", ""),
    )

    # Create messages with system prompt
    messages = [SystemMessage(content=system_prompt)] + state["messages"]

    # Get routing decision with structured output
    router = llm.with_structured_output(RouteDecision)
    decision = router.invoke(messages)

    return {"next_agent": decision.next}
