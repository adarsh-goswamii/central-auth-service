import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    env: str            = os.getenv("ENV", "local")
    db_user: str        = os.getenv("DB_USER", "user")
    db_password: str    = os.getenv("DB_PASSWORD", "user")
    db_host: str        = os.getenv("DB_HOST", "0.0.0.0")
    db_name: str        = os.getenv("DB_NAME", "central_db")

@lru_cache
def get_settings():
    return BaseConfig()