from fastapi_plus.service.base import BaseService

from ..dao.demo import DemoDao
from ..model.demo import Demo


class DemoService(BaseService):
    def __init__(self, auth_data: dict = {}):
        user_id = auth_data.get('user_id', 0)
        self.Model = Demo
        self.dao = DemoDao(user_id)
        self.dao.Model = Demo

        super().__init__(user_id, auth_data)
