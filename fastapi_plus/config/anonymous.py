"""
匿名访问接口列表
格式：req.method + req.url.path，其中method为大写
"""
anonymous_path_list = [
    'GET/',
    'GET/robots.txt',
    'GET/favicon.ico',
    'GET/docs',
    'GET/docs/oauth2-redirect',
    'GET/redoc',
    'GET/openapi.json',
    'GET/sys_info',
]
