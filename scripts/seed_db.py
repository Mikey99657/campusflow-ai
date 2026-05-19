"""Seed script to populate database with sample data."""

import asyncio
from app.db.base import get_session_factory, init_db
from app.db.models.task import Task


async def seed():
    """Create sample tasks."""
    await init_db()

    factory = get_session_factory()
    async with factory() as session:
        # Sample tasks
        tasks = [
            Task(
                title="Binary Search Implementation",
                description="Implement binary search algorithm in Java",
                task_type="code_generation",
                user_id=1,
            ),
            Task(
                title="Data Structures Lab Report",
                description="Write a lab report on linked list operations",
                task_type="lab_report",
                user_id=1,
            ),
            Task(
                title="Class Diagram for Library System",
                description="Design a UML class diagram for a library management system",
                task_type="uml_analysis",
                user_id=1,
            ),
        ]

        session.add_all(tasks)
        await session.commit()

        print(f"Created {len(tasks)} sample tasks.")


if __name__ == "__main__":
    asyncio.run(seed())
