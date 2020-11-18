from datetime import datetime
from typing import List, Dict

from pydantic import BaseModel

from ..utils.json_encoders import JSONEncoders


class BaseSchema(BaseModel):
    class Config:
        json_encoders = JSONEncoders.json_encoders


class RespBaseSchema(BaseModel):
    code: int = 0
    message: str = 'SUCCESS'


class RespIdSchema(RespBaseSchema):
    id: int = 0


class RespDetailSchema(RespBaseSchema):
    detail: dict = None


class RespListSchema(RespBaseSchema):
    page: int = 0
    size: int = 0
    total: int = 0
    page_total: int = 0
    list: List[Dict] = None


class ListFilterSchema(BaseModel):
    key: str
    condition: str
    value: str


class ListOrderSchema(BaseModel):
    key: str
    condition: str


class ListKeySchema(BaseModel):
    key: str
    rename: str


class ListArgsSchema(BaseModel):
    page: int = 1
    size: int = 10
    keywords: str = None
    is_deleted: str = None
    user_id: int = None
    filters: List[ListFilterSchema] = None
    orders: List[ListOrderSchema] = None
    keys: List[ListKeySchema] = None


class UserBaseSchema(BaseSchema):
    id: int = None
    name: str = None

    class Config:
        orm_mode = True


class FileBaseSchema(BaseModel):
    id: int
    name: str
    suffix: str

    class Config:
        orm_mode = True


class InfoSchema(BaseSchema):
    id: int = None
    parent_id: int = None
    type: int = None
    sort: int = None
    status: int = None
    code: str = None
    name: str = None
    label: str = None
    logo: str = None
    url: str = None
    info: str = None
    remark: str = None

    class Config:
        orm_mode = True


class DetailSchema(InfoSchema):
    created_time: datetime
    updated_time: datetime
