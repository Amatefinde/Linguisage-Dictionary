from pydantic_settings import BaseSettings
from pydantic import BaseModel
from dotenv import load_dotenv

import os

load_dotenv()


class Settings(BaseSettings):
    DB_HOST: str = os.environ.get("DB_HOST")
    DB_PORT: str = os.environ.get("DB_PORT")
    DB_NAME: str = os.environ.get("DB_NAME")
    DB_USER: str = os.environ.get("DB_USER")
    DB_PASS: str = os.environ.get("DB_PASS")

    db_url: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    db_echo: bool = False

    api_v1_prefix: str = "/api/v1"

    # content_manager_url: str = os.environ.get("CONTENT_MANAGER_URL")
    # neural_module_url: str = os.environ.get("NEURAL_MODULE_URL")
    URL_TO_WORD_LIST: str = os.environ.get("URL_TO_WORD_LIST")
    DICTIONARY_BASE_URL: str = os.environ.get("DICTIONARY_BASE_URL")


settings = Settings()
