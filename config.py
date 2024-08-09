import datetime
import logging

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

scheduler_setting = {
    'jobstores': {
        'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
    },
    'job_defaults': {
        'coalesce': True,
        'max_instances': 1,
        'misfire_grace_time': None
    }}

scheduler = AsyncIOScheduler(job_defaults=scheduler_setting['job_defaults'], jobstores=scheduler_setting['jobstores'],
                             timezone=datetime.UTC)

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]',
                    datefmt='%d/%m/%Y %I:%M:%S', encoding='utf-8')
