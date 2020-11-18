from fastapi import APIRouter
from starlette.responses import Response

base_router = APIRouter()


@base_router.get('/')
async def get_root():
    """
    访问根路径
    """
    return Response(content='', media_type='text/plain')


@base_router.get('/robots.txt')
async def get_robots():
    """
    获取爬虫权限
    """
    return Response(content='User-agent: * \nDisallow: /', media_type='text/plain')


@base_router.get('/sys_info')
async def get_sys_info():
    """
    获取系统基本信息
    """
    from ..service.sys_info import SysInfoService

    return SysInfoService().get_sys_info()
