import logging
import os
from pathlib import Path

from fastapi import APIRouter, status, Depends, UploadFile, HTTPException
from fastapi.responses import FileResponse

from api.file_router.dependencies import get_file_by_id
from databases.models import FileModel
from databases.queries.orm import AsyncORM
from files.s3 import s3

router = APIRouter(prefix="/files", tags=["Files"])
UPLOAD_DIR = Path("files/downloaded/")


@router.post("/upload/", response_model=None, status_code=status.HTTP_201_CREATED, description="Uploads file on server")
async def saving_file(file: UploadFile) ->\
        HTTPException | dict[str, str]:
    """
    Uploads file on server
    :param file: Any video, image or document
    """

    try:
        with open(UPLOAD_DIR / file.filename, "wb") as f:
            while chunk := await file.read(1024):
                f.write(chunk)

        await s3.upload_file(file_path=f"{UPLOAD_DIR}/{file.filename}")

    except Exception as ex:
        logging.error(ex)
        raise HTTPException(status_code=500, detail="File cannot be uploaded")

    else:
        await AsyncORM.create_file(size_kb=file.size, file_format=file.filename.split('.')[-1], filename=file.filename)
        return {"message": f"File {file.filename} has been downloaded successfully"}


@router.get("/download/", status_code=status.HTTP_200_OK, description="Sends the file by UUID")
async def download_file_by_id(file: FileModel = Depends(get_file_by_id)) -> FileResponse:
    """
    Sends the file by UUID
    :param file: File on the server
    :return: File from the server
    """

    return FileResponse(UPLOAD_DIR / file.filename, media_type="application/octet-stream",
                        filename=file.filename)
