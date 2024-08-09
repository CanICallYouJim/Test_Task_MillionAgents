import logging
import os

from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from databases.database import get_async_session
from databases.models import FileModel


async def clean_old_files(session: AsyncSession = Depends(get_async_session)):
    """
    Deletes old files
    :param session: DB session
    """
    subquery = select(FileModel.id).order_by(FileModel.created_at.desc()).limit(10)

    filenames = await session.execute(delete(FileModel).where(FileModel.id.not_in(subquery)).returning(FileModel.filename))
    await session.commit()

    counter = 0
    for filename in filenames:
        try:
            os.remove(f"downloaded/{filename}")
            counter += 1
        except:
            continue

    logging.info(f"{len(filenames)} were deleted from DB, {counter} were deleted locally")
