import datetime
import decimal

from json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):
    """
    自定义JSON编码处理
    :version: 1.1
    :date: 2019-01-08
    """

    def default(self, obj):
        try:
            if isinstance(obj, datetime.date):
                return obj.isoformat().replace('T', ' ')
            elif isinstance(obj, datetime.datetime):
                return obj.isoformat().replace('T', " ")
            elif isinstance(obj, decimal.Decimal):
                return str(obj)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
