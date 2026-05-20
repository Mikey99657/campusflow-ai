import json
import re
from langchain_core.messages import SystemMessage, AIMessage

from app.agents.state import AgentState
from app.agents.prompts.loader import load_prompt
from app.core.llm_factory import create_llm


VALID_AGENTS = {"coding_agent", "report_agent", "uml_agent", "summary_agent", "FINISH"}


def parse_route_from_response(response) -> str:
    """Extract routing decision from model response."""
    content = response.content if isinstance(response, AIMessage) else str(response)

    # Try to find JSON with routing field
    json_match = re.search(r'\{[^}]+\}', content)
    if json_match:
        try:
            data = json.loads(json_match.group())
            route = data.get("routing") or data.get("route_to") or data.get("next") or data.get("route")
            if route:
                # Case-insensitive match
                for agent in VALID_AGENTS:
                    if route.lower() == agent.lower():
                        return agent
        except json.JSONDecodeError:
            pass

    # Try to find agent name in text
    content_lower = content.lower()
    for agent in VALID_AGENTS:
        if agent.lower() in content_lower:
            return agent

    return "coding_agent"


def supervisor_node(state: AgentState) -> dict:
    """Supervisor node: routes requests to specialist agents."""
    # Check round count to prevent infinite loops
    round_count = state.get("round_count", 0)
    if round_count >= 1:
        return {"next_agent": "FINISH", "round_count": round_count + 1}

    llm = create_llm(temperature=0)

    # Load supervisor prompt
    system_prompt = load_prompt(
        "supervisor_system",
        context_summary=state.get("context_summary", ""),
    )

    # Create messages with system prompt
    messages = state["messages"]
    all_messages = [SystemMessage(content=system_prompt)] + messages

    # Get routing decision
    response = llm.invoke(all_messages)
    next_agent = parse_route_from_response(response)

    return {"next_agent": next_agent, "round_count": round_count + 1}
