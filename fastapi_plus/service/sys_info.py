import platform


class SysInfoService(object):
    """信息信息服务类.

    获取服务运行系统的基础信息
    """

    @staticmethod
    def get_sys_info():
        return {
            'platform': platform.platform(),
            'machine': platform.machine(),
            'node': platform.node(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
        }
