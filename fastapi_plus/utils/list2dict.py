"""
list2dict, list转换为dict
:version: 1.0
:date: 2020-02-15
"""


def list_list2dict(x_list: list, key_index: int = 0, value_index: int = 1):
    x_dict = {}

    for x_item in x_list:
        if isinstance(x_item, list) or isinstance(x_item, tuple):
            if x_item[key_index]:
                x_dict[x_item[key_index]] = x_item[value_index]

    return x_dict


def list_dict2dict(x_list: list, key_key: str, value_key: str):
    x_dict = {}

    for x_item in x_list:
        if isinstance(x_item, dict):
            if key_key in x_item and value_key in x_item:
                x_dict[x_item[key_key]] = x_item[value_key]

    return x_dict
