from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin


class MeasureTypeMySQL(db.Model, SerializerMixin):
    __tablename__ = 'measure_type'
    __table_args__ = {'schema': 'calibration'}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    descr = db.Column(db.String)
