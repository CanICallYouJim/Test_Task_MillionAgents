import datetime
import uuid
from typing import Annotated

from sqlalchemy import text

from .database import Base1
from sqlalchemy.orm import Mapped, mapped_column, relationship

created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class FileModel(Base1):
    __tablename__ = "files"
    repr_cols_num = 4

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    size_kb: Mapped[int]
    file_format: Mapped[str]
    filename: Mapped[str]
    created_at: Mapped[created_at]