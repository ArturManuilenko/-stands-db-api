from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin


class LaboratoryMySQL(db.Model, SerializerMixin):
    __tablename__ = 'laboratory'
    __table_args__ = {'schema': 'calibration'}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    descr = db.Column(db.String)
