import logging

from fastapi import APIRouter, status, Depends, UploadFile, HTTPException
from fastapi.responses import FileResponse

from api.file_router.dependencies import get_file_by_id
from databases.models import FileModel
from databases.queries.orm import AsyncORM

router = APIRouter(prefix="/files", tags=["Files"])


@router.post("/upload/", response_model=None)
async def saving_file(file: UploadFile) ->\
        HTTPException | dict[str, str]:
    """
    Uploads file on server
    :param file: Any video, image or document
    :param session: DB connection
    """
    try:
        with open(f"files/downloaded/{file.filename}", "wb") as f:
            f.write(await file.read())
    except Exception as ex:
        logging.error(ex)
        raise HTTPException(status_code=500, detail="File cannot be uploaded")
    else:
        await AsyncORM.create_file(size_kb=file.size, file_format=file.filename.split('.')[-1], filename=file.filename)
        return {"message": f"File {file.filename} has been downloaded successfully"}


@router.get("/download/", status_code=status.HTTP_200_OK)
async def download_file_by_id(file: FileModel = Depends(get_file_by_id)) -> FileResponse:
    """
    Sends the file by UUID
    :param file: File on the server
    :return: File from the server
    """
    return FileResponse(f"files/downloaded/{file.filename}", media_type="application/octet-stream", filename=file.filename)
