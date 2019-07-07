import redis
from configs import settings
from . import myjson


class RedisCache(object):
    def __init__(self):
        self.conn = redis.Redis(connection_pool=redis.ConnectionPool(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=settings.REDIS_DECODE_RESPONSE
        ))

    def expire_cache(self, key, time=5*3600):
        key = "{}_{}".format(settings.REDIS_PRE, key)
        self.conn.expire(key, time)

    def delete_cache(self, key):
        """
        删除key键
        :param key:
        :return:
        """
        key = "{}_{}".format(settings.REDIS_PRE, key)
        conn = self.conn
        for k in conn.scan_iter(match=key):
            conn.delete(k)

    def set_cache(self, key, val, ex=5*3600):
        key = "{}_{}".format(settings.REDIS_PRE, key)
        if isinstance(val, dict):
            val = myjson.dumps(val)
        self.conn.setex(key, val, ex)

    def get_cache(self, key):
        key = "{}_{}".format(settings.REDIS_PRE, key)
        conn = self.conn
        for k in conn.scan_iter(key):
            temp = conn.get(k)
            if temp:
                try:
                    res = myjson.loads(temp)
                except:
                    res = temp
                return res

    def srem_cache(self, val):
        conn = self.conn
        if isinstance(val, str):
            val = str.encode(val)
        conn.srem(val)
