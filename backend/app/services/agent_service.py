import json
from typing import AsyncGenerator

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from app.agents.supervisor import get_supervisor_graph
from app.agents.state import AgentState


async def run_agent_stream(
    message: str,
    conversation_id: int | None = None,
    thread_id: str | None = None,
) -> AsyncGenerator[dict, None]:
    """Run the agent graph and yield SSE events.

    Args:
        message: User message
        conversation_id: Optional conversation ID
        thread_id: Optional thread ID for state persistence

    Yields:
        SSE event dictionaries
    """
    graph = get_supervisor_graph()

    # Prepare config with thread_id for checkpointer
    config = {"configurable": {"thread_id": thread_id or "default"}}

    # Initial state
    initial_state: AgentState = {
        "messages": [HumanMessage(content=message)],
        "next_agent": "",
        "task_type": "",
        "context_summary": "",
        "metadata": {"conversation_id": conversation_id},
    }

    # Yield thinking event
    yield {
        "event": "agent_thinking",
        "data": {"agent": "supervisor", "content": "Analyzing your request..."}
    }

    try:
        # Stream graph execution
        async for event in graph.astream(initial_state, config=config):
            for node_name, node_output in event.items():
                if node_name == "supervisor":
                    # Supervisor routing decision
                    next_agent = node_output.get("next_agent", "")
                    if next_agent and next_agent != "FINISH":
                        yield {
                            "event": "agent_thinking",
                            "data": {"agent": next_agent, "content": f"Routing to {next_agent}..."}
                        }

                elif node_name in ["coding_agent", "report_agent", "uml_agent", "summary_agent"]:
                    # Agent output
                    messages = node_output.get("messages", [])
                    for msg in messages:
                        if isinstance(msg, AIMessage) and msg.content:
                            yield {
                                "event": "agent_message",
                                "data": {
                                    "agent": node_name,
                                    "content": msg.content,
                                    "delta": msg.content,
                                }
                            }

                            # Check for tool calls
                            if hasattr(msg, "tool_calls") and msg.tool_calls:
                                for tool_call in msg.tool_calls:
                                    yield {
                                        "event": "tool_call",
                                        "data": {
                                            "agent": node_name,
                                            "tool": tool_call.get("name", ""),
                                            "input": str(tool_call.get("args", "")),
                                        }
                                    }

                elif node_name == "__end__":
                    # Graph execution complete
                    yield {
                        "event": "done",
                        "data": {
                            "conversation_id": conversation_id,
                            "status": "completed",
                        }
                    }

    except Exception as e:
        yield {
            "event": "error",
            "data": {"message": str(e)}
        }
