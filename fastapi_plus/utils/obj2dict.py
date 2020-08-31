"""
object与dict转换函数
:version: 1.1
:date: 2019-01-08
"""


def obj2dict(obj):
    if not obj:
        return None

    # 判断是否是Query
    # 定义一个字典对象
    dictionary = {}
    # 检索记录中的成员
    for field in [x for x in dir(obj) if
                  # 过滤属性
                  not x.startswith('_')
                  # 过滤掉方法属性
                  and hasattr(obj.__getattribute__(x), '__call__') == False
                  # 过滤掉不需要的属性
                  and x != 'metadata'
                  and x != 'query']:
        data = obj.__getattribute__(field)

        if hasattr(data, 'query'):
            data = obj2dict(data)

        try:
            dictionary[field] = data
        except TypeError:
            dictionary[field] = None

    # 返回字典对象
    return dictionary
