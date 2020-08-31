import time

from .redis import RedisUtils


class Locker(object):
    """
    Locker 基于redis的锁
    :version: 1.2
    :date: 2020-02-11
    """

    redis = RedisUtils()

    # 判断是否存在锁
    @staticmethod
    def has_lock(key):
        return Locker.redis.get_string('locker:' + key)

    # 加锁
    @staticmethod
    def lock(key, expiration=None):
        Locker.redis.set_string('locker:' + key, str(time.time()), expiration)

    # 解锁
    @staticmethod
    def unlock(key):
        Locker.redis.delete('locker:' + key)
