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
        "round_count": 0,
    }

    # Yield thinking event
    yield {
        "event": "agent_thinking",
        "data": {"agent": "supervisor", "content": "Analyzing your request..."}
    }

    try:
        # Use ainvoke to get the final result (avoids streaming internal ReAct iterations)
        result = await graph.ainvoke(initial_state, config=config)

        # Determine which agent responded
        messages = result.get("messages", [])
        agent_name = result.get("next_agent", "coding_agent")

        # Find the last AI message (the agent's final response)
        last_ai_msg = None
        for msg in messages:
            if isinstance(msg, AIMessage) and msg.content:
                last_ai_msg = msg

        if last_ai_msg:
            yield {
                "event": "agent_thinking",
                "data": {"agent": agent_name, "content": f"Routing to {agent_name}..."}
            }
            yield {
                "event": "agent_message",
                "data": {
                    "agent": agent_name,
                    "content": last_ai_msg.content,
                    "delta": last_ai_msg.content,
                }
            }

        # Done
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
