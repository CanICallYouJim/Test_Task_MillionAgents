import logging
import os
from pathlib import Path

from sqlalchemy import delete, select

from databases.database import async_session
from databases.models import FileModel


async def clean_old_files():
    """
    Deletes old files
    :param session: DB session
    """
    async with async_session() as session:
        subquery = select(FileModel.id).order_by(FileModel.created_at.desc()).limit(3)

        filenames = await session.scalars(delete(FileModel).where(FileModel.id.not_in(subquery)).returning(FileModel.filename))
        await session.commit()

    counter = 0
    filenames = filenames.all()
    script_dir = Path(__file__).parent

    for filename in filenames:
        try:
            file_path = script_dir / f"downloaded/{filename}"
            os.remove(file_path)
            counter += 1
        except Exception as ex:
            logging.error(ex)
            continue

    logging.info(f"{len(filenames)} were deleted from DB, {counter} were deleted locally")
