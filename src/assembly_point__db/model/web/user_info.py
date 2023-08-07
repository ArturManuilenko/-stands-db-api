from db_utils import CustomQuery
from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin
from src.assembly_point__db.model.web.web_access import WebAccess


class UserInfo(db.Model, SerializerMixin):
    __tablename__ = 'user_info'
    __table_args__ = {'schema': 'web'}
    id = db.Column(db.Integer, db.ForeignKey("web.web_access.id"), primary_key=True)
    id_model = db.relationship(
        WebAccess,
        foreign_keys=[id],
        query_class=CustomQuery,
        uselist=False,
        lazy='joined'
    )
    fio = db.Column(db.String(1024))
