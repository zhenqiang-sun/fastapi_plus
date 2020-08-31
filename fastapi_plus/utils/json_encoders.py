from datetime import datetime


class JSONEncoders(object):
    json_encoders = {
        datetime: lambda dt: dt.isoformat(' ')
    }
