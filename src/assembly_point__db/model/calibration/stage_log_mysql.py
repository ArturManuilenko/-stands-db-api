from db_utils import CustomQuery
from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin

from src.assembly_point__db.model.calibration.report_mysql import ReportMySQL


class StageLogMySQL(db.Model, SerializerMixin):
    __tablename__ = 'stage_log'
    __table_args__ = {'schema': 'calibration'}
    id = db.Column(db.Integer, primary_key=True)
    report = db.Column(db.Integer, db.ForeignKey("calibration.report.id"))
    report_model = db.relationship(
        ReportMySQL,
        foreign_keys=[report],
        query_class=CustomQuery,
        uselist=False,
        lazy='joined')
    number = db.Column(db.Integer)
    name = db.Column(db.String)
    log = db.Column(db.String)
    result = db.Column(db.String(20))
