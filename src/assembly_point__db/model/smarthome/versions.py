from db_utils import CustomQuery
from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin
from src.assembly_point__db.model.stend_control_schema.device_id_descr import DeviceIdDescr


class Versions(db.Model, SerializerMixin):
    __tablename__ = 'versions'
    __table_args__ = {'schema': 'smarthome'}
    number = db.Column(db.Integer, primary_key=True, unique=True)
    id = db.Column(db.Integer, db.ForeignKey("stend_control_schema.device_id_descr.id"))
    id_model = db.relationship(
        DeviceIdDescr,
        foreign_keys=[id],
        query_class=CustomQuery,
        uselist=False,
        lazy='joined'
    )
    version = db.Column(db.Integer)
    variant = db.Column(db.Integer)
    hard = db.Column(db.Integer)
    open_time = db.Column(db.DateTime)
    close_time = db.Column(db.DateTime)
    allow = db.Column(db.Boolean)
