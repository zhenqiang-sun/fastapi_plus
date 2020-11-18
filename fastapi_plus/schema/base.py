from datetime import datetime
from typing import List, Dict

from pydantic import BaseModel

from ..utils.json_encoders import JSONEncoders


class BaseSchema(BaseModel):
    """
    基础Schema
    """

    class Config:
        json_encoders = JSONEncoders.json_encoders  # 使用自定义json转换


class BaseObjSchema(BaseModel):
    """
    基础ObjSchema
    """

    class Config:
        json_encoders = JSONEncoders.json_encoders
        orm_mode = True  # 为模型实例


class RespBaseSchema(BaseModel):
    """
    基础返回Schema
    """
    code: int = 0  # 返回编号
    message: str = 'SUCCESS'  # 返回消息


class RespIdSchema(RespBaseSchema):
    """
    返回Schema，带id
    """
    id: int = 0  # 返回id


class RespDetailSchema(RespBaseSchema):
    """
    详情返回Schema
    """
    detail: dict = None  # 返回详情


class RespListSchema(RespBaseSchema):
    """
    列表返回Schema
    """
    page: int = 0  # 当前页码
    size: int = 0  # 每页大小
    count: int = 0  # 数据总条数
    page_count: int = 0  # 总页数
    list: List[Dict] = None  # 数据list


class ListFilterSchema(BaseModel):
    """
    列表参数：过滤条件Schema
    """
    key: str  # 字段名
    condition: str  # 过滤条件
    value: str  # 条件值，如condition为in或!in时，value为用“,”分割的多值得字符串


class ListOrderSchema(BaseModel):
    """
    列表参数：排序条件Schema
    """
    key: str  # 字段名
    condition: str  # 排序条件


class ListKeySchema(BaseModel):
    """
    列表参数：字段条件Schema
    """
    key: str  # 字段名
    rename: str = None  # 字段名重命名, 为空则不进行重命名


class ListArgsSchema(BaseModel):
    """
    列表参数Schema
    """
    page: int = 1  # 当前页码
    size: int = 10  # 每页条数
    keywords: str = None  # 关键字，用于模糊、分词搜索
    is_deleted: str = None  # 软删标记
    user_id: int = None  # 数据对应用户id
    filters: List[ListFilterSchema] = None  # 过滤条件
    orders: List[ListOrderSchema] = None  # 排序条件
    keys: List[ListKeySchema] = None  # 字段条件


class UserBaseSchema(BaseObjSchema):
    """
    用户基础Schema
    """
    id: int = None  # 用户id
    name: str = None  # 用户名称


class FileBaseSchema(BaseObjSchema):
    """
    文件基础Schema
    """
    id: int  # 文件id
    name: str  # 文件名称
    suffix: str  # 文件后缀


class InfoSchema(BaseObjSchema):
    """
    详情基础Schema
    """
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


class DetailSchema(InfoSchema):
    """
    详情基础Schema
    """
    created_time: datetime
    updated_time: datetime
