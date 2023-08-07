from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin


class LogUpdateMySQL(db.Model, SerializerMixin):
    __tablename__ = 'log_update'
    __table_args__ = {'schema': 'work'}
    id = db.Column(db.Integer, primary_key=True)
    stend = db.Column(db.Integer)
    name = db.Column(db.String(45))
    type = db.Column(db.String(45))
    md5 = db.Column(db.String(32))
    time = db.Column(db.DateTime)
    version = db.Column(db.String(45))
    source = db.Column(db.String)
    descr = db.Column(db.String)
