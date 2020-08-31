from datetime import datetime

from pydantic import BaseModel

from ..utils.json_encoders import JSONEncoders


class BaseSchema(BaseModel):
    class Config:
        json_encoders = JSONEncoders.json_encoders


class ResponseSchema(BaseModel):
    code: int = 0
    message: str = 'SUCCESS'
    id: int = None


class ListArgsSchema(BaseModel):
    page_now: int = 1
    page_size: int = 10
    keywords: str = None
    user_id: int = None
    relation_obj: str = None
    relation_id: int = None


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


class ListSchema(BaseSchema):
    id: int
    name: str
    remark: str
    created_time: datetime
    updated_time: datetime

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
