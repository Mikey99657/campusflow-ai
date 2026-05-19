from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings


class Base(DeclarativeBase):
    """SQLAlchemy declarative base."""
    pass


engine = None
async_session_factory = None


def get_engine():
    global engine
    if engine is None:
        settings = get_settings()
        engine = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.DEBUG,
        )
    return engine


def get_session_factory():
    global async_session_factory
    if async_session_factory is None:
        async_session_factory = async_sessionmaker(
            get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return async_session_factory


async def get_db() -> AsyncSession:
    """Dependency: get database session."""
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_db():
    """Initialize database tables."""
    from app.db.models import user, conversation, message, task, workflow  # noqa: F401

    async with get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
