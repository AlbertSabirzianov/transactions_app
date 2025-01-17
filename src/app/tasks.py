import asyncio

from celery import Celery

from .settings import RedisSettings
from .services import save_new_statistic_to_db

redis_settings = RedisSettings()

celery_app = Celery('tasks', broker=redis_settings.redis_url)


@celery_app.task
def statistic_task():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(save_new_statistic_to_db())


