from abc import ABC, abstractmethod

from pydantic_settings import BaseSettings
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

# # Настройка пути к .env
# ENV_MODE = "production"  # Менять на "production" для основного .env
# env_file = ".env.local" if ENV_MODE == "local" else ".env"
# env_path = PROJECT_ROOT / env_file
# #
# # # Загрузка переменных окружения
# load_dotenv(dotenv_path=env_path)

ENV = ".env.local"

class Settings(BaseSettings):
    # Channel
    CHANNEL_NAME: str
    CHANNEL_ID: int

    # Bot
    BOT_TOKEN: str
    ADMIN: str

    # Database
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: int
    DATABASE_HOST: str

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: str

    # AI
    OPENROUTER_API_KEY: str


def get_settings() -> Settings:
    env = ENV
    env_path = PROJECT_ROOT / env
    return Settings(_env_file=env_path, _env_file_encoding='utf-8')


settings = get_settings()
