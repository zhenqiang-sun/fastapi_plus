from fastapi import APIRouter
from starlette.responses import Response

base_router = APIRouter()


@base_router.get('/')
async def get_root():
    return Response(content='', media_type='text/plain')


@base_router.get('/robots.txt')
async def get_robots():
    return Response(content='User-agent: * \nDisallow: /', media_type='text/plain')


@base_router.get('/sys_info')
async def get_sys_info():
    from ..service.sys_info import SysInfoService

    return SysInfoService().get_sys_info()
