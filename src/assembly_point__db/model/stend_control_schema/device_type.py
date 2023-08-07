from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin


class DeviceType(db.Model, SerializerMixin):
    __tablename__ = 'device_type'
    __table_args__ = {'schema': 'stend_control_schema'}
    id = db.Column(db.Integer, primary_key=True, unique=True)
    mac_table = db.Column(db.String)
    name = db.Column(db.String)
    mac_start = db.Column(db.Integer)
    mac_end = db.Column(db.Integer)
    pool_table = db.Column(db.String(45))
