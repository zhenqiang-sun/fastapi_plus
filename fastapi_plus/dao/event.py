import json

from ..model.event_log import EventLog
from ..utils.db import DbUtils
from ..utils.json_custom import CustomJSONEncoder
from ..utils.obj2json import obj2json


class EventDao(object):
    """Event(事件)Dao，业务事件记录.

    用于业务事件记录，比如修改数据等

    Attributes:
        user_id: 当前操作用户id
        db: db实体
    """

    def __init__(self, user_id: int = 0):
        self.user_id = user_id
        self.db = DbUtils()

    def get_event_log(self, event_id: int, relation_obj: str, before_data=None) -> EventLog:
        """
        生成事件记录对象并返回
        :param event_id: 事件id
        :param relation_obj: 相关对象
        :param before_data: 之前数据
        :return: 事件记录对象
        """

        # 构造数据：事件记录实例
        event_log = EventLog()
        event_log.user_id = self.user_id
        event_log.event_id = event_id
        event_log.relation_obj = relation_obj

        if before_data:
            event_log.relation_id = before_data.id
            event_log.before_data = obj2json(before_data)

        return event_log

    def create_event_log(self, event_log: EventLog, after_data=None):
        """
        创建事件记录，保存在数据库中
        :param event_log: 事件记录实例
        :param after_data: 变化后的数据
        """
        if after_data:
            event_log.after_data = obj2json(after_data)

        if not event_log.change_data:
            self.calculate_change(event_log)

        self.db.sess.add(event_log)
        self.db.sess.flush()

    def update_event_log(self, event_log: EventLog):
        """
        更新操作记录
        :param event_log:
        :return:
        """
        self.db.sess.add(event_log)
        self.db.sess.flush()

    @staticmethod
    def calculate_change(event_log: EventLog):
        """
        比较数据前后差异，计算变化部分
        :param event_log:
        """
        if not event_log.before_data or not event_log.after_data:
            event_log.change_data = None
            return None

        before: dict = json.loads(event_log.before_data)
        after: dict = json.loads(event_log.after_data)
        change = {}

        for key in before:
            if key == 'updated_time':
                continue

            if before[key] != after[key]:
                change[key] = {
                    'before': before.get(key),
                    'after': after.get(key),
                }

        if not change:
            event_log.change_data = None
        else:
            event_log.change_data = json.dumps(change, ensure_ascii=False, cls=CustomJSONEncoder)
