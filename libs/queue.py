import redis

from config import REDIS, TIMOUT
from libs.exception import MoreThanOneVideoException

pool = redis.BlockingConnectionPool(**REDIS, max_connections=1, timeout=5)


def start_video(chat_id):
    db = redis.Redis(connection_pool=pool)
    if db.get(has_video(chat_id)):
        raise MoreThanOneVideoException()

    db.set(has_video(chat_id), 1, ex=TIMOUT)
    db.close()


def stop_video(chat_id):
    pass


def has_video(chat_id):
    return f"video:::{chat_id}"
