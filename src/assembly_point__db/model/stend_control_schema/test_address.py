from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin


class TestAddress(db.Model, SerializerMixin):
    __tablename__ = 'test_address'
    __table_args__ = {'schema': 'stend_control_schema'}

    mac = db.Column(db.Integer, unique=True)
    serial = db.Column(db.Integer, unique=True)
    datetime = db.Column(db.DateTime)
