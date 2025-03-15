
from pydantic_settings import BaseSettings


class Settings(
    BaseSettings,
    env_file=".env",
    env_file_encoding="utf-8",
    extra="allow",
):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    db_host: str = "localhost"
    db_port: int = 5432
    db_echo: bool = False

    @property
    def db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.db_host}:{self.db_port}/{self.postgres_db}"
        )


def get_env_settings() -> Settings:
    return Settings()
