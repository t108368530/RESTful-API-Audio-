import logging
import sys
from typing import Optional

from loguru import logger
from pydantic import BaseSettings
from webservice.core.logging import InterceptHandler
from redis import StrictRedis ,ConnectionPool


class Settings(BaseSettings):
    DEV_MOD: Optional[str] = None
    REDIS_HOST: Optional[str] = None
    REDIS_PASSWORD: Optional[str] = None
    REDUS_UNIX_SOCKET_PATH: Optional[str] = None
    REDIS_PORT: Optional[str] = None
    QUEUE_NAME: Optional[str] = None
    QUEUE_NAME_2: Optional[str] = None
    

    class Config:
        env_file: str = ".env"


settings = Settings()


LOGGING_LEVEL = logging.DEBUG if settings.DEV_MOD == "true" else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access", "fastapi")

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(
    handlers=[
        {
            "sink": sys.stderr,
            "level": LOGGING_LEVEL,
        }
    ]
)


message_queue = StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    db=0,
)

message_queue2 = StrictRedis(
    unix_socket_path=settings.REDUS_UNIX_SOCKET_PATH,
    password=settings.REDIS_PASSWORD,
    max_connections=2000,
    db=0,
)

# pool=ConnectionPool(
#     unix_socket_path=settings.REDUS_UNIX_SOCKET_PATH,
#     password=settings.REDIS_PASSWORD,
#     max_connections=10000,
#     db=0,
# )
# message_queue3 = StrictRedis(connection_pool=pool)