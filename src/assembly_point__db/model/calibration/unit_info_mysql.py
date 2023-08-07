from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin


class UnitInfoMySQL(db.Model, SerializerMixin):
    __tablename__ = 'unit_info'
    __table_args__ = {'schema': 'calibration'}
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    place = db.Column(db.String)
    descr = db.Column(db.String)
