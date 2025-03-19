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
    pg_host: str = "localhost"
    pg_port: int = 5432
    pg_echo: bool = False

    redis_host: str
    redis_port: int
    redis_db: int = 0

    @property
    def postgres_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.pg_host}:{self.pg_port}/{self.postgres_db}"
        )

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    @classmethod
    def get_settings(cls):
        return cls()
