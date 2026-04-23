from functools import lru_cache

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    RABBITMQ_USER: Optional[str] = None
    RABBITMQ_PASS: Optional[str] = None
    RABBITMQ_HOST: Optional[str] = None
    RABBITMQ_PORT: Optional[int] = None
    MODEL_HOST: Optional[str] = None
    MODEL_NAME: Optional[str] = None
    HOST_APP: Optional[str] = None

@lru_cache
def get_settings():
    return Settings()