from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin


class ProcedureMySQL(db.Model, SerializerMixin):
    __tablename__ = 'procedure'
    __table_args__ = {'schema': 'calibration'}
    id = db.Column(db.Integer, primary_key=True)
    algoritm_id = db.Column(db.Integer, db.ForeignKey("calibration.algoritm.id"))
    unit_id = db.Column(db.Integer, db.ForeignKey("calibration.unit.id"))
    mac = db.Column(db.Integer)
    serial = db.Column(db.String)
    factory = db.Column(db.String)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    result = db.Column(db.String)
