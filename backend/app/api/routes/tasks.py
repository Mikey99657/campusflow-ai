from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.api.deps import DbSession
from app.api.schemas.task import TaskCreate, TaskResponse, TaskListResponse
from app.db.models.task import Task

router = APIRouter()


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    db: DbSession,
    status: str | None = None,
    task_type: str | None = None,
    limit: int = 20,
    offset: int = 0,
):
    """List tasks with optional filters."""
    query = select(Task)

    if status:
        query = query.where(Task.status == status)
    if task_type:
        query = query.where(Task.task_type == task_type)

    query = query.order_by(Task.created_at.desc()).offset(offset).limit(limit)

    result = await db.execute(query)
    tasks = result.scalars().all()

    return TaskListResponse(tasks=tasks, total=len(tasks))


@router.post("", response_model=TaskResponse)
async def create_task(db: DbSession, task_data: TaskCreate):
    """Create a new task."""
    task = Task(
        title=task_data.title,
        description=task_data.description,
        task_type=task_data.task_type,
        user_id=1,  # TODO: get from auth
    )
    db.add(task)
    await db.flush()
    await db.refresh(task)
    return task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(db: DbSession, task_id: int):
    """Get task by ID."""
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.delete("/{task_id}")
async def delete_task(db: DbSession, task_id: int):
    """Delete task."""
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(task)
    return {"status": "deleted"}
