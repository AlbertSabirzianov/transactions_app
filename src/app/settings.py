from pydantic_settings import BaseSettings


class DbSettings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int

    @property
    def postgres_url(self):
        return (
            f""
            f"postgresql+asyncpg://"
            f"{self.postgres_user}:{self.postgres_password}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


class RedisSettings(BaseSettings):
    redis_url: str = "redis://redis:6379/0"


class AppSettings(BaseSettings):
    api_key: str


