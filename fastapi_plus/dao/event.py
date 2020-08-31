import json

from ..model.event_log import EventLog
from ..utils.db import DbUtils
from ..utils.json_custom import CustomJSONEncoder
from ..utils.obj2json import obj2json


class EventDao:
    def __init__(self, user_id: int = 0):
        self.user_id = user_id
        self.db = DbUtils()

    def get_event_log(self, event_id: int, relation_obj: str, before_data=None) -> EventLog:
        event_log = EventLog()
        event_log.user_id = self.user_id
        event_log.event_id = event_id
        event_log.relation_obj = relation_obj

        if before_data:
            event_log.relation_id = before_data.id
            event_log.before_data = obj2json(before_data)

        return event_log

    def create_event_log(self, event_log: EventLog, after_data=None):
        if after_data:
            event_log.after_data = obj2json(after_data)

        if not event_log.change_data:
            self.calculate_change(event_log)

        self.db.sess.add(event_log)
        self.db.sess.flush()

    def update_event_log(self, event_log: EventLog):
        self.db.sess.add(event_log)
        self.db.sess.flush()

    @staticmethod
    def calculate_change(event_log: EventLog):
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
