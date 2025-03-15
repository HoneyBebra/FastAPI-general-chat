from functools import lru_cache
from logging import config as logging_config
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

from ..core.logger import LOGGING

load_dotenv()

BASE_DIR = Path(__file__).parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")

    app_name: str = "Service"
    app_description: str = "Description"
    app_version: str = "0.0.1"

    app_port: int = 8000

    log_level: str = "INFO"

    # These parameters also need to be changed in the nginx and docker settings
    api_v1_prefix: str = "/api/v1"

    postgres_user: str = "user"
    postgres_password: str = "password"
    postgres_host: str = "postgres"
    postgres_port: str = "5432"
    postgres_db: str = "db"

    postgres_echo: bool = True

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.postgres_user}:"
            f"{self.postgres_password}@"
            f"{self.postgres_host}:"
            f"{self.postgres_port}/"
            f"{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


settings = get_settings()

logging_config.dictConfig(LOGGING)
