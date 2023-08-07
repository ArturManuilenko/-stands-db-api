from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin


class AlgoritmMySQL(db.Model, SerializerMixin):
    __tablename__ = 'algoritm'
    __table_args__ = {'schema': 'calibration'}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    stage_count = db.Column(db.Integer)
    descr = db.Column(db.String)
