from langgraph.graph import StateGraph, START, END

from app.agents.state import AgentState
from app.agents.nodes.supervisor_node import supervisor_node
from app.agents.nodes.coding_agent import build_coding_agent
from app.agents.nodes.report_agent import build_report_agent
from app.agents.nodes.uml_agent import build_uml_agent
from app.agents.nodes.summary_agent import build_summary_agent
from app.core.checkpointer import get_checkpointer


def route_after_supervisor(state: AgentState) -> str:
    """Conditional edge: routes to the agent chosen by supervisor."""
    return state["next_agent"]


def build_supervisor_graph():
    """Build the main multi-agent supervisor graph.

    Graph topology:
        START -> supervisor -> [coding_agent | report_agent | uml_agent | summary_agent | FINISH]
                                      |                |              |              |
                                      +--------+-------+-------+-----+-------+------+
                                               v                v              v
                                              END              END            END

    Each agent responds once, then ends.
    """
    # Build specialist sub-agents
    coding_agent = build_coding_agent()
    report_agent = build_report_agent()
    uml_agent = build_uml_agent()
    summary_agent = build_summary_agent()

    # Assemble the graph
    builder = StateGraph(AgentState)

    # Add nodes
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("coding_agent", coding_agent)
    builder.add_node("report_agent", report_agent)
    builder.add_node("uml_agent", uml_agent)
    builder.add_node("summary_agent", summary_agent)

    # Add edges
    builder.add_edge(START, "supervisor")
    builder.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {
            "coding_agent": "coding_agent",
            "report_agent": "report_agent",
            "uml_agent": "uml_agent",
            "summary_agent": "summary_agent",
            "FINISH": END,
        },
    )

    # All agents go directly to END (no looping)
    builder.add_edge("coding_agent", END)
    builder.add_edge("report_agent", END)
    builder.add_edge("uml_agent", END)
    builder.add_edge("summary_agent", END)

    # Compile with checkpointer for state persistence
    checkpointer = get_checkpointer()
    return builder.compile(checkpointer=checkpointer)


# Global graph instance
_supervisor_graph = None


def get_supervisor_graph():
    """Get or create the supervisor graph singleton."""
    global _supervisor_graph
    if _supervisor_graph is None:
        _supervisor_graph = build_supervisor_graph()
    return _supervisor_graph
