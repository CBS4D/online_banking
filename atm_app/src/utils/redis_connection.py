import redis
import os

from src.config import get_config


config_env = os.getenv("ENV", "development")
app_config = get_config(config_env)

redis_connection = redis.StrictRedis(
    host=app_config.get("REDIS_HOST"),
    port=app_config.get("REDIS_PORT"),
    db=app_config.get("REDIS_DB"),
    decode_responses=True
)

# print(redis_connection)

# redis_connection.set("test", "redis connected")