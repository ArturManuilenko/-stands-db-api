from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin


class DeviceIdDescr(db.Model, SerializerMixin):
    __tablename__ = 'device_id_descr'
    __table_args__ = {'schema': 'stend_control_schema'}
    id = db.Column(db.Integer, primary_key=True, unique=True)
    description = db.Column(db.String(256), unique=True)
