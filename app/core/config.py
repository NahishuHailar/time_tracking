from abc import ABC, abstractmethod

from pydantic_settings import BaseSettings


class BaseSettingsConfig(
    BaseSettings,
    ABC,
    env_file=".env",
    env_file_encoding="utf-8",
    extra="allow",
):
    @property
    @abstractmethod
    def url(self) -> str:
        pass

    @classmethod
    def get_settings(cls):
        return cls()


class PostgresSettings(BaseSettingsConfig):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    pg_host: str = "localhost"
    pg_port: int = 5432
    pg_echo: bool = False

    @property
    def url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.pg_host}:{self.pg_port}/{self.postgres_db}"
        )

class RedisSettings(BaseSettingsConfig):
    redis_host: str
    redis_port: int
    redis_db: int = 0

    @property
    def url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"
