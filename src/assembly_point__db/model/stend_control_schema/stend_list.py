from db_utils import CustomQuery
from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin
from src.assembly_point__db.model.stend_control_schema.device_type import DeviceType


class StendList(db.Model, SerializerMixin):
    __tablename__ = 'stend_list'
    __table_args__ = {'schema': 'stend_control_schema'}

    stend_id = db.Column(db.Integer, primary_key=True, unique=True)
    device_id = db.Column(db.Integer, db.ForeignKey("stend_control_schema.device_type.id"))
    device_model = db.relationship(
        DeviceType,
        foreign_keys=[device_id],
        query_class=CustomQuery,
        uselist=False,
        lazy='joined'
    )
    generate = db.Column(db.Integer)
    description = db.Column(db.String)
