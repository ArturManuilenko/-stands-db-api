from db_utils import CustomQuery
from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin
from src.assembly_point__db.model.stend_control_schema.stend_list import StendList


class StendCrc(db.Model, SerializerMixin):
    __tablename__ = 'stend_crc'
    __table_args__ = {'schema': 'stend_control_schema'}

    id = db.Column(db.Integer, db.ForeignKey("stend_control_schema.stend_list.stend_id"), primary_key=True, unique=True)
    id_model = db.relationship(
        StendList,
        foreign_keys=[id],
        query_class=CustomQuery,
        uselist=False,
        lazy='joined'
    )
    time = db.Column(db.DateTime)
    param = db.Column(db.Integer)
    platform = db.Column(db.Integer)
