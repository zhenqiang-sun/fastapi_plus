from fastapi import Header

from .redis import RedisUtils


async def get_auth_data(authorization: str = Header(None)):
    """
    获取登录用户认证数据, 通常用于controller层
    :param authorization: 请求header中的authorization
    :return:
    """
    return get_auth_data_by_authorization(authorization)


def get_auth_data_by_authorization(authorization: str, ex: int = None):
    """
    获取登录用户认证数据
    :param authorization:
    :param prefix: 前缀
    :param ex: 数据过期秒数
    :return:
    """
    if authorization:
        return get_auth_data_by_token(authorization, ex)

    return None


def get_auth_data_by_token(token: str, ex: int = None):
    """
    获取登录用户认证数据， 从redis中读取
    :param token: 登录的token
    :param ex: 数据过期秒数
    :return: 登录认证数据
    """

    auth_data = RedisUtils().get('token:' + token)

    if ex and auth_data:
        RedisUtils().expire('token:' + token, ex)

    return auth_data


def update_auth_data(auth_data: dict, ex: int = None):
    """
    更新认证数据
    :param auth_data: 登录认证数据
    :param ex: 数据过期秒数
    """
    RedisUtils().set('token:' + auth_data.get('token'), auth_data, ex)
