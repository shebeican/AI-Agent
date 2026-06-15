import os
from typing import Optional, List

from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(PROJECT_PATH, f".env.{os.getenv('PYTHON_ENV', 'dev')}"),
        env_file_encoding='utf-8'
    )

    # 讯飞星辰APIKEY
    XF_API_KEY: str


settings = Settings()
