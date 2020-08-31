from typing import List

from sqlalchemy import and_
from sqlalchemy import text

from ..schema.base import ListArgsSchema
from ..utils.db import DbUtils


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

    def read_list(self, args: ListArgsSchema) -> List[Model]:
        filter_relation_obj = text('')
        filter_relation_id = text('')
        filter_search = text('')

        if args.relation_obj and hasattr(self.Model, 'relation_obj'):
            filter_relation_obj = self.Model.relation_obj == args.relation_obj

            if args.relation_id and hasattr(self.Model, 'relation_id'):
                filter_relation_id = self.Model.relation_id == args.relation_id

        if args.keywords and hasattr(self.Model, 'search'):
            filter_search = and_(*[self.Model.search.like('%' + kw + '%') for kw in args.keywords.split(' ')])

        list = self.db.sess.query(self.Model).filter(
            self.Model.is_deleted == 0,
            self.Model.user_id == args.user_id,
            filter_relation_obj,
            filter_relation_id,
            filter_search
        ).order_by(
            self.Model.updated_time.desc()
        ).offset((args.page_now - 1) * args.page_size).limit(args.page_size).all()

        return list

    def update(self, model: Model):
        self.db.sess.add(model)
        self.db.sess.flush()

    def delete(self, model: Model):
        model.is_deleted = 1
        self.update(model)
