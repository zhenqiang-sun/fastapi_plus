import platform


class SysInfoService:
    @staticmethod
    def get_sys_info():
        return {
            'platform': platform.platform(),
            'machine': platform.machine(),
            'node': platform.node(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
        }
