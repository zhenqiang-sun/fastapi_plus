from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session


class DbConfig(object):
    """
    DbConfig DB配置类
    :version: 1.4
    :date: 2020-02-11
    """

    driver = 'mysql+pymysql'
    host = 'mariadb'
    port = '3306'
    username = 'root'
    password = ''
    database = ''
    charset = 'utf8mb4'
    table_name_prefix = ''
    echo = True
    pool_size = 100
    max_overflow = 100
    pool_recycle = 60

    def get_url(self):
        config = [
            self.driver,
            '://',
            self.username,
            ':',
            self.password,
            '@',
            self.host,
            ':',
            self.port,
            '/',
            self.database,
            '?charset=',
            self.charset,
        ]

        return ''.join(config)


class DbUtils(object):
    """
    DbUtils DB工具类
    :version: 1.4
    :date: 2020-02-11
    """

    sess: Session = None
    default_config: DbConfig = None

    def __init__(self, config: DbConfig = None):
        if not config:
            config = self.default_config

        self.sess = self._create_scoped_session(config)

    def __del__(self):
        self.sess.close()

    @staticmethod
    def _create_scoped_session(config: DbConfig):
        engine = create_engine(
            config.get_url(),
            pool_size=config.pool_size,
            max_overflow=config.max_overflow,
            pool_recycle=config.pool_recycle,
            echo=config.echo
        )

        session_factory = sessionmaker(autocommit=True, autoflush=False, bind=engine)

        return scoped_session(session_factory)

    # 根据文件获取SQL文件
    @staticmethod
    def get_sql_by_file(file_path, params={}):
        sql = DbUtils._get_file(file_path)
        return sql.format(**params)

    # 获取SQL文件
    @staticmethod
    def _get_file(file_path):
        with open('app/sql/' + file_path, 'r', encoding='utf-8') as f:
            return f.read()
