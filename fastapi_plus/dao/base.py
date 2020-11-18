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
        self.db.sess.add(model)
        self.db.sess.flush()

    def read(self, id: int) -> Model:
        return self.db.sess.query(self.Model).filter(
            self.Model.id == id,
            self.Model.is_deleted == 0,
            self.Model.user_id == self.user_id,
        ).first()

    def update(self, model: Model):
        self.db.sess.add(model)
        self.db.sess.flush()

    def delete(self, model: Model):
        model.is_deleted = 1
        self.update(model)

    def read_list(self, args: ListArgsSchema) -> RespListSchema:
        filters = []

        if args.is_deleted != 'all':
            filters.append(self.Model.is_deleted == 0)

        if args.user_id:
            filters.append(self.Model.user_id == args.user_id)

        filters.extend(self._handle_list_filters(args.filters))

        if args.keywords and hasattr(self.Model, 'search'):
            filters.append(and_(*[self.Model.search.like('%' + kw + '%') for kw in args.keywords.split(' ')]))

        query = self.db.sess.query(self.Model).filter(*filters)
        total = query.count()

        if total > 0:
            orders = self._handle_list_orders(args.orders)
            obj_list = query.order_by(*orders).offset((args.page - 1) * args.size).limit(args.size).all()
        else:
            obj_list = []

        resp = RespListSchema()
        resp.page = args.page
        resp.size = args.size
        resp.total = total
        resp.page_total = math.ceil(total / args.size)
        resp.list = self._handle_list_keys(args.keys, obj_list)

        return resp

    def _handle_list_filters(self, args_filters: ListFilterSchema):
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
        orders = []

        if args_orders:
            for item in args_orders:
                if hasattr(self.Model, item.key):
                    attr = getattr(self.Model, item.key)

                    if item.condition == 'desc':
                        orders.append(attr.desc())
                    elif item.condition == 'acs':
                        orders.append(attr)
                    elif item.condition == 'rand':
                        orders.append(func.rand())

        return orders

    def _handle_list_keys(self, args_keys: ListKeySchema, obj_list: List):
        keys = []

        if args_keys:
            for item in args_keys:
                if hasattr(self.Model, item.key):
                    keys.append(item)

        resp_list = []

        for obj in obj_list:
            dict_1 = obj2dict(obj)

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
