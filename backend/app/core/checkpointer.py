from langgraph.checkpoint.memory import MemorySaver

from app.config import get_settings


def get_checkpointer():
    """Get a checkpointer instance for workflow state persistence.

    Uses in-memory checkpointer for development.
    Can be swapped to PostgresSaver for production.
    """
    settings = get_settings()

    # In-memory checkpointer for development
    # For production: from langgraph.checkpoint.postgres import PostgresSaver
    return MemorySaver()
