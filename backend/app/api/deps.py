from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.db.base import get_db


# Database session dependency
DbSession = Annotated[AsyncSession, Depends(get_db)]
