from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin


class LoraKeysMySQL(db.Model, SerializerMixin):
    __tablename__ = 'lora_keys'
    __table_args__ = {'schema': 'work'}
    mac = db.Column(db.BigInteger, primary_key=True)
    group = db.Column(db.Integer)
    key = db.Column(db.String(64))
    datetime = db.Column(db.DateTime)
