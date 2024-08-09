import uvicorn

from databases.queries.orm import AsyncORM
from fastapi import FastAPI
from contextlib import asynccontextmanager
from api import router
from config import scheduler
from files.cron_cleaning import clean_old_files


@asynccontextmanager
async def lifespan(app: FastAPI):
    await AsyncORM.create_tables()
    scheduler.add_job(clean_old_files, 'cron', hour=12, id='clean_old_files_id', replace_existing=True)
    scheduler.start()
    yield

app = FastAPI(
    title='Million Agents',
    version="1.0.1",
    lifespan=lifespan
)

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run('main:app')
