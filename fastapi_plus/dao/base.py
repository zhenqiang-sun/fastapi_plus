import math
from typing import List

from sqlalchemy import and_, func

from ..schema.base import ListArgsSchema, ListOrderSchema, ListKeySchema, ListFilterSchema, RespListSchema
from ..utils.db import DbUtils
from ..utils.obj2dict import obj2dict


class BaseDao(object):
    """Base(基础)Dao，用于被继承.

    CRUD基础Dao类，拥有基本方法，可直接继承使用

    Attributes:
        user_id: 当前操作用户id
        db: db实体
    """
    Model = None

    def __init__(self, user_id=0):
        self.user_id = user_id
        self.db = DbUtils()

    def create(self, model: Model):
        """
        创建一条数据
        :param model: 数据模型实例
        """
        self.db.sess.add(model)
        self.db.sess.flush()

    def read(self, id: int, user_id: int = None, is_deleted: int = 0) -> Model:
        """
        读取一条数据
        :param id: 数据id
        :param user_id: 用户id
        :param is_deleted: 是否为已删除数据
        :return: 数据模型实例
        """

        # 定义：query过滤条件
        filters = []

        # 判断：软删标记
        if is_deleted == 1:
            filters.append(self.Model.is_deleted == 1)
        elif is_deleted == 2:
            pass
        else:
            filters.append(self.Model.is_deleted == 0)

        # 判断：是否限制指定用户的数据
        if user_id:
            filters.append(self.Model.user_id == user_id)

        return self.db.sess.query(self.Model).filter(
            self.Model.id == id,
            *filters
        ).first()

    def update(self, model: Model):
        """
        更新一条数据
        :param model: 数据模型实例
        :return:
        """
        self.db.sess.add(model)
        self.db.sess.flush()

    def delete(self, model: Model):
        """
        删除一条数据，软删除
        :param model: 数据模型实体
        """
        model.is_deleted = 1
        self.update(model)

    def read_list(self, args: ListArgsSchema) -> RespListSchema:
        """
        读取数据列表
        :param args: 聚合参数，详见：ListArgsSchema
        :return: 返回数据列表结构，详见：RespListSchema
        """

        # 定义：query过滤条件
        filters = []

        # 判断：是否包含已软删除的数据
        if args.is_deleted != 'all':
            filters.append(self.Model.is_deleted == 0)

        # 判断：是否限制指定用户的数据
        if args.user_id:
            filters.append(self.Model.user_id == args.user_id)

        # 增加：传入调整
        filters.extend(self._handle_list_filters(args.filters))

        # 判断：是否进行关键词搜索
        if args.keywords and hasattr(self.Model, 'search'):
            filters.append(and_(*[self.Model.search.like('%' + kw + '%') for kw in args.keywords.split(' ')]))

        # 执行：数据检索
        query = self.db.sess.query(self.Model).filter(*filters)
        count = query.count()

        # 判断： 结果数，是否继续查询
        if count > 0:
            orders = self._handle_list_orders(args.orders)
            obj_list = query.order_by(*orders).offset((args.page - 1) * args.size).limit(args.size).all()
        else:
            obj_list = []

        # 构造：返回结构
        resp = RespListSchema()
        resp.page = args.page
        resp.size = args.size
        resp.count = count
        resp.page_count = math.ceil(count / args.size)  # 计算总页数
        resp.list = self._handle_list_keys(args.keys, obj_list)  # 处理list

        return resp

    def _handle_list_filters(self, args_filters: ListFilterSchema):
        """
        处理list接口传入的过滤条件
        :param args_filters: 传入过滤条件
        :return: 转换后的sqlalchemy过滤条件
        """
        filters = []

        if args_filters:
            for item in args_filters:
                if hasattr(self.Model, item.key):
                    attr = getattr(self.Model, item.key)

                    if item.condition == '=':
                        filters.append(attr == item.value)
                    elif item.condition == '!=':
                        filters.append(attr != item.value)
                    elif item.condition == '<':
                        filters.append(attr < item.value)
                    elif item.condition == '>':
                        filters.append(attr > item.value)
                    elif item.condition == '<=':
                        filters.append(attr <= item.value)
                    elif item.condition == '>=':
                        filters.append(attr >= item.value)
                    elif item.condition == 'like':
                        filters.append(attr.like('%' + item.value + '%'))
                    elif item.condition == 'in':
                        filters.append(attr.in_(item.value.split(',')))
                    elif item.condition == '!in':
                        filters.append(~attr.in_(item.value.split(',')))
                    elif item.condition == 'null':
                        filters.append(attr.is_(None))
                    elif item.condition == '!null':
                        filters.append(~attr.isnot(None))

        return filters

    def _handle_list_orders(self, args_orders: ListOrderSchema):
        """
        处理list接口传入的排序条件
        :param args_orders: 传入排序条件
        :return: 转换后的sqlalchemy排序条件
        """
        orders = []

        if args_orders:
            for item in args_orders:
                if hasattr(self.Model, item.key):
                    attr = getattr(self.Model, item.key)

                    if item.condition == 'desc':
                        orders.append(attr.desc())
                    elif item.condition == 'acs':
                        orders.append(attr)
                    elif item.condition == 'rand':  # 随机排序
                        orders.append(func.rand())

        return orders

    def _handle_list_keys(self, args_keys: ListKeySchema, obj_list: List):
        """
        处理list返回数据，根据传入参数keys进行过滤
        :param args_keys: 传入过滤字段
        :return: 转换后的list数据，数据转为dict类型
        """
        keys = []

        if args_keys:
            for item in args_keys:
                if hasattr(self.Model, item.key):
                    keys.append(item)

        resp_list = []

        for obj in obj_list:
            dict_1 = obj2dict(obj)

            # 判断：keys存在，不存在则返回所有字段
            if keys:
                dict_2 = {}
                for item in keys:
                    if item.rename:
                        dict_2[item.rename] = dict_1[item.key]
                    else:
                        dict_2[item.key] = dict_1[item.key]
            else:
                dict_2 = dict_1

            resp_list.append(dict_2)

        return resp_list
