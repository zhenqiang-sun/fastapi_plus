import json
import time

from starlette.requests import Request
from starlette.responses import Response

from .auth import get_auth_data_by_authorization, get_auth_data_by_token
from .list2dict import list_list2dict
from .mongo import MongoUtils
from .obj2dict import obj2dict


class Log(object):
    id = None
    status = 1
    user_id = None
    in_datetime = None
    in_millisecond = None
    out_datetime = None
    out_millisecond = None
    use_millisecond = None
    ip = None
    url = None
    method = None
    path = None
    path_params = None
    query_params = None
    header = None  # request.headers.items()
    body = None
    response_status_code = None
    response = None


async def create_log(request: Request) -> Log:
    mongo_log = MongoUtils().get_collection('request_log')

    in_time = time.time()
    log = Log()
    log.status = 1
    log.in_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(in_time))
    log.in_millisecond = int(round(in_time * 1000))
    log.ip = request.client.host
    log.url = str(request.url)
    log.method = request.method
    log.path = request.url.path
    log.path_params = request.path_params
    log.query_params = request.url.query
    log.header = list_list2dict(request.headers.items())

    try:
        log.body = await request.json()
    except:
        pass

    if 'authorization' in log.header:
        auth_data = get_auth_data_by_authorization(log.header['authorization'])

        if auth_data:
            log.user_id = auth_data.get('user_id')

    mongo_result = mongo_log.insert_one(obj2dict(log))
    log.id = mongo_result.inserted_id

    return log


async def update_log(log: Log, response: Response):
    mongo_log = MongoUtils().get_collection('request_log')

    out_time = time.time()
    log.status = 2
    log.out_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(out_time))
    log.out_millisecond = int(round(out_time * 1000))
    log.use_millisecond = log.out_millisecond - log.in_millisecond
    log.response_status_code = response.status_code

    try:
        log.response = json.loads(str(response.body, 'utf8'))
    except:
        pass

    if not log.user_id and log.response and 'token' in log.response:
        auth_data = get_auth_data_by_token(log.response['token'])
        log.user_id = auth_data.get('user_id')

    mongo_log.update_one({'_id': log.id}, {'$set': obj2dict(log)})
