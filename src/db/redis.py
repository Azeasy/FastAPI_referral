import redis
from src.core.config import settings

redis = redis.from_url(settings.REDIS_URL, decode_responses=True)


async def get_cache():
    return redis
