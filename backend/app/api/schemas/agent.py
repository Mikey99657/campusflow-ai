from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    conversation_id: int | None = None
    agent_type: str = Field(default="supervisor", pattern="^(supervisor|coding|report|uml|summary)$")


class ChatResponse(BaseModel):
    conversation_id: int
    message: str


class AgentInfo(BaseModel):
    name: str
    description: str
    capabilities: list[str]


class StreamEvent(BaseModel):
    event: str  # agent_thinking, agent_message, tool_call, agent_done, done
    data: dict
