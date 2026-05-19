from langgraph.checkpoint.sqlite import SqliteSaver

from app.config import get_settings


def get_checkpointer():
    """Get a checkpointer instance for workflow state persistence.

    Uses SQLite for development, can be swapped to PostgreSQL for production.
    """
    settings = get_settings()

    # For SQLite-based checkpointer
    # In production, use PostgresSaver.from_conn_string(settings.DATABASE_URL)
    return SqliteSaver.from_conn_string(":memory:")
