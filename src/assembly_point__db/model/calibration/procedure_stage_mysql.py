from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin


class ProcedureStageMySQL(db.Model, SerializerMixin):
    __tablename__ = 'procedure_stage'
    __table_args__ = {'schema': 'calibration'}
    id = db.Column(db.Integer, primary_key=True)
    proc_id = db.Column(db.Integer, db.ForeignKey("calibration.procedure.id"))
    number = db.Column(db.Integer)
    name = db.Column(db.String)
    report = db.Column(db.String)
    result = db.Column(db.String)
