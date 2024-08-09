import logging
import os
from pathlib import Path

from sqlalchemy import delete, select

from databases.database import async_session
from databases.models import FileModel
from files.s3 import s3


async def clean_old_files():
    """
    Deletes old files
    :param session: DB session
    """
    async with async_session() as session:
        subquery = select(FileModel.id).order_by(FileModel.created_at.desc()).limit(15)

        filenames = await session.scalars(delete(FileModel).where(FileModel.id.not_in(subquery)).returning(FileModel.filename))
        await session.commit()

    filenames = filenames.all()
    script_dir = Path(__file__).parent

    counter_local = 0
    counter_s3 = 0

    for filename in filenames:
        try:
            file_path = script_dir / f"downloaded/{filename}"

            os.remove(file_path)
            counter_local += 1

            s3.delete_file(file_path)
            counter_s3 += 1

        except Exception as ex:
            logging.error(ex)
            continue

    logging.info(f"{len(filenames)} were deleted from DB, {counter_local} were deleted locally, {counter_s3} from S3")
