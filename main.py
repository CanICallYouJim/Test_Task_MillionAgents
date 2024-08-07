import uvicorn

from databases.queries.orm import AsyncORM
from fastapi import FastAPI
from contextlib import asynccontextmanager
from api import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await AsyncORM.create_tables()
    yield

app = FastAPI(
    title='Million Agents',
    version="1.0.1",
    lifespan=lifespan
)

app.include_router(router)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
