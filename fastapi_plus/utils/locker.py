import time

from .redis import RedisUtils


class Locker(object):
    """
    Locker 基于redis的锁
    :version: 1.2
    :date: 2020-02-11
    """

    redis: RedisUtils

    def __init__(self):
        self.redis = RedisUtils()

    # 判断是否存在锁
    def has_lock(self, key):
        return self.redis.get_string('locker:' + key)

    # 加锁
    def lock(self, key, expiration=None):
        self.redis.set_string('locker:' + key, str(time.time()), expiration)

    # 解锁
    def unlock(self, key):
        self.redis.delete('locker:' + key)
