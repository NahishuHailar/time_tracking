from pydantic_settings import BaseSettings


class EnvSettings(
    BaseSettings,
    env_file=".env",
    env_file_encoding="utf-8",
    extra="allow",
):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_echo: bool = False

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    @property
    def postgres_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    @classmethod
    def get_settings(cls):
        return cls()
