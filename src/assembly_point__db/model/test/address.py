from db_utils import CustomQuery
from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin
from src.assembly_point__db.model.test.chip_type import ChipType


class Address(db.Model, SerializerMixin):
    __tablename__ = 'address'
    __table_args__ = {'schema': 'test'}
    mac = db.Column(db.Integer, unique=True)
    serial = db.Column(db.String(32), unique=True)
    datetime = db.Column(db.DateTime)
    chip_id = db.Column(db.Integer, db.ForeignKey("test.chip_type.id"))
    chip_id_model = db.relationship(
        ChipType,
        foreign_keys=[chip_id],
        query_class=CustomQuery,
        uselist=False,
        lazy='joined'
    )
