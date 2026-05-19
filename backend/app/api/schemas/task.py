from datetime import datetime
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    task_type: str = Field(..., pattern="^(code_generation|lab_report|uml_analysis|learning_summary|custom)$")


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    task_type: str
    status: str
    priority: int
    result: str | None
    error_message: str | None
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None

    model_config = {"from_attributes": True}


class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int
