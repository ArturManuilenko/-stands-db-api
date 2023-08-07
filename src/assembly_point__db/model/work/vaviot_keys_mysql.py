from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin


class VaviotKeysMySQL(db.Model, SerializerMixin):
    __tablename__ = 'vaviot_keys'
    __table_args__ = {'schema': 'work'}
    mac = db.Column(db.Integer, db.ForeignKey('work.address_fluo.mac'), primary_key=True)
    group = db.Column(db.Integer)
    key = db.Column(db.String(64))
    datetime = db.Column(db.DateTime)
