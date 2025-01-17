from fastapi import FastAPI
from app.settings import DbSettings, RedisSettings, AppSettings
from app.api_router import api_router
from app.services import create_tables


def create_app() -> FastAPI:
    DbSettings()
    AppSettings()
    RedisSettings()

    fastapi_app = FastAPI()
    fastapi_app.include_router(api_router)

    @fastapi_app.on_event("startup")
    async def startup_event():
        await create_tables()

    return fastapi_app


app = create_app()


