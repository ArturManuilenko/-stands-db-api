from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin


class ProtocolMySQL(db.Model, SerializerMixin):
    __tablename__ = 'protocol'
    __table_args__ = {'schema': 'calibration'}
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String)
    fio = db.Column(db.String)
    t = db.Column(db.Float)
    f = db.Column(db.Float)
    p = db.Column(db.Float)
    lab = db.Column(db.Integer)
    time = db.Column(db.DateTime)
