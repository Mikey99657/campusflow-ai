import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.services.agent_service import run_agent_stream

router = APIRouter()


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    conversation_id: int | None = None
    agent_type: str = Field(default="supervisor", pattern="^(supervisor|coding|report|uml|summary)$")


@router.post("/chat")
async def chat(request: ChatRequest):
    """Send message to agent and get SSE stream response.

    Uses LangGraph supervisor pattern to route tasks to specialist agents.
    Returns Server-Sent Events for real-time streaming.
    """
    async def generate_events():
        async for event in run_agent_stream(
            message=request.message,
            conversation_id=request.conversation_id,
        ):
            yield f"event: {event['event']}\ndata: {json.dumps(event['data'])}\n\n"

    return StreamingResponse(
        generate_events(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/capabilities")
async def get_capabilities():
    """List available agents and their capabilities."""
    return {
        "agents": [
            {
                "name": "supervisor",
                "description": "Routes tasks to specialist agents",
                "capabilities": ["task_routing", "multi_agent_coordination"]
            },
            {
                "name": "coding_agent",
                "description": "Java code generation and analysis",
                "capabilities": ["java_generation", "code_analysis", "debugging"]
            },
            {
                "name": "report_agent",
                "description": "Lab report and summary generation",
                "capabilities": ["lab_report", "learning_summary", "academic_writing"]
            },
            {
                "name": "uml_agent",
                "description": "UML diagram analysis and generation",
                "capabilities": ["class_diagram", "sequence_diagram", "uml_analysis"]
            },
            {
                "name": "summary_agent",
                "description": "Learning summaries and course notes",
                "capabilities": ["learning_summary", "course_notes", "study_guides"]
            },
        ]
    }
