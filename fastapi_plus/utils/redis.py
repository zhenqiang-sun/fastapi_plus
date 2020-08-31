import json

from redis import ConnectionPool, Redis

from .json_custom import CustomJSONEncoder


class RedisConfig(object):
    """
    RedisConfig Redis配置类
    :version: 1.2
    :date: 2020-02-11
    """

    host = 'redis'
    port = '6379'
    username = 'root'
    password = ''
    database = 0
    max_connections = 100


class RedisUtils:
    """
    RedisUtils redis工具类
    :version: 1.2
    :date: 2020-02-11
    """

    _conn = None
    _default_conn_pool = None
    default_config: RedisConfig = None

    def __init__(self, config: RedisConfig = None):
        if config:
            self._conn = self._get_conn(config)
        else:
            if not self._default_conn_pool:
                RedisUtils._default_conn_pool = self._create_pool(self.default_config)

            self._conn = Redis(connection_pool=self._default_conn_pool)

    @staticmethod
    def _create_pool(config: RedisConfig):
        return ConnectionPool(
            host=config.host,
            port=config.port,
            max_connections=config.max_connections,
            username=config.username,
            password=config.password,
            db=config.database
        )

    @staticmethod
    def _get_conn(config: RedisConfig):
        return Redis(
            host=config.host,
            port=config.port,
            max_connections=config.max_connections,
            username=config.username,
            password=config.password,
            db=config.database
        )

    def delete(self, key):
        return self._conn.delete(key)

    def set_string(self, key, value, ex=None):
        return self._conn.set(key, value, ex)

    def get_string(self, key):
        value = self._conn.get(key)

        if value:
            return str(value, 'utf-8')
        else:
            return None

    def set(self, key, value, ex=None):
        return self._conn.set(key, json.dumps(value, ensure_ascii=False, cls=CustomJSONEncoder), ex)

    def get(self, key):
        value = self._conn.get(key)

        if value:
            return json.loads(str(value, 'utf-8'))
        else:
            return None

    def expire(self, key, ex=int):
        return self._conn.expire(key, ex)
