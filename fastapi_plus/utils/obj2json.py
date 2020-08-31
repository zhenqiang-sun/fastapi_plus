"""
object转换json string函数
:version: 1.0
:date: 2020-02-16
"""
import json

from .json_custom import CustomJSONEncoder
from .obj2dict import obj2dict


def obj2json(obj) -> str:
    x_dict = obj2dict(obj)
    x_json = json.dumps(x_dict, ensure_ascii=False, cls=CustomJSONEncoder)

    # 返回json字符串
    return x_json
