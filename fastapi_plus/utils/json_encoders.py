from datetime import datetime


class JSONEncoders(object):
    """
    定义JSONEncoders
    """
    json_encoders = {
        datetime: lambda dt: dt.isoformat(' ')  # 解决日期和时间中“T”字符的格式问题
    }
