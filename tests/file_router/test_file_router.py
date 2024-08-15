import os
import uuid
from pathlib import Path

import pytest
from sqlalchemy import select

from databases.queries.orm import AsyncORM
from databases.models import FileModel
from databases.database import async_session

files_path = Path("files/for_tests")


@pytest.fixture(scope="session", autouse=True)
async def clean_tables():
    await AsyncORM.create_tables()


class TestFile:
    test_file = "testdata.docx"

    @classmethod
    async def test_post_saving_file_positive(cls, ac):
        response = await ac.post("/files/upload/", files={"file": (cls.test_file, open(files_path / cls.test_file, 'rb'))})
        assert response.status_code == 201

    @staticmethod
    async def test_post_saving_file_negative(ac):
        response = await ac.post("/files/upload/", json={})
        assert response.status_code == 422

    @classmethod
    async def test_get_download_file_positive(cls, ac):
        async with async_session() as session:
            file_id = await session.scalar(select(FileModel.id).filter_by(filename=cls.test_file))
        response = await ac.get(f"/files/download/?file_id={file_id}")
        assert response.status_code == 200

    @classmethod
    async def test_get_download_file_negative(cls, ac):
        response = await ac.get(f"/files/download/?file_id={uuid.uuid4()}")
        assert response.status_code == 404
        assert response.json() == {'detail': 'File was not found'}
