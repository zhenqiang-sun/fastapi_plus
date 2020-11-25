from fastapi_plus.model.base import *


class Demo(Base):
    __tablename__ = 'demo'
    __table_args__ = {'comment': 'Demo'}

    user_id = Column(BIGINT(20), nullable=False, server_default=text("0"), comment='用户ID')
    category_id = Column(BIGINT(20), nullable=False, server_default=text("0"), comment='分类ID')
    category_name = Column(String(255), nullable=False, server_default=text("''"), comment='分类名称')
    data = Column(String(1000), nullable=False, server_default=text("''"), comment='数据')
