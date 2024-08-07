import uuid

from fastapi import HTTPException

from databases.database import Base1, engine, async_session, settings
from ..models import FileModel


class AsyncORM:
    @staticmethod
    async def create_tables():
        async with engine.begin() as conn:
            if settings.MODE == "TEST":
                await conn.run_sync(Base1.metadata.drop_all)
            await conn.run_sync(Base1.metadata.create_all)

    @staticmethod
    async def create_file(size_kb: int, file_format: str, filename: str):
        async with async_session() as session:
            try:
                instance = FileModel(id=uuid.uuid4(), size_kb=size_kb, file_format=file_format, filename=filename)
                session.add(instance)
                await session.commit()
            except:
                raise HTTPException(status_code=500, detail="File metadata saving failed")
