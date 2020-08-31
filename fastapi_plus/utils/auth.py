from fastapi import Header

from .redis import RedisUtils


async def get_auth_data(authorization: str = Header(None)):
    return get_auth_data_by_authorization(authorization)


def get_auth_data_by_authorization(authorization: str, ex: int = None):
    if authorization:
        return get_auth_data_by_token(authorization[3:])

    return None


def get_auth_data_by_token(token: str, ex: int = None):
    auth_data = RedisUtils().get('token:' + token)

    if ex and auth_data:
        RedisUtils().expire('token:' + token, ex)

    return auth_data


def update_auth_data(auth_data: dict):
    RedisUtils().set('token:' + auth_data.get('token'), auth_data)
