import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    db_host: str = "localhost"
    db_port: int = 5432
    db_echo: bool = False

    model_config = SettingsConfigDict(
        env_file=f".env.test" if os.getenv("TESTING") == "true" else ".env",    
        env_file_encoding="utf-8",
        extra="allow",
    )

    @property
    def db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.db_host}:{self.db_port}/{self.postgres_db}"
        )

def get_env_settings() -> Settings:
    return Settings()

settings = get_env_settings()
