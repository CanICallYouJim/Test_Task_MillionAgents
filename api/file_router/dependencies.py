from uuid import UUID

from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from databases.database import get_async_session
from databases.models import FileModel


async def get_file_by_id(file_id: UUID, session: AsyncSession = Depends(get_async_session)):
    res = await session.get(FileModel, file_id)
    if not res:
        raise HTTPException(status_code=404, detail="File was not found")

    return res
