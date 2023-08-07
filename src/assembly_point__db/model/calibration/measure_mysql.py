from db_utils import CustomQuery
from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin

from src.assembly_point__db.model.calibration.report_mysql import ReportMySQL


class MeasureMySQL(db.Model, SerializerMixin):
    __tablename__ = 'measure'
    __table_args__ = {'schema': 'calibration'}
    id = db.Column(db.Integer, primary_key=True)
    report = db.Column(db.Integer, db.ForeignKey("calibration.report.id"))
    report_model = db.relationship(
        ReportMySQL,
        foreign_keys=[report],
        query_class=CustomQuery,

        uselist=False,
        lazy='joined')
    group = db.Column(db.String(5))
    type = db.Column(db.String(45))
    phase = db.Column(db.String(5))
    error = db.Column(db.Float)
    value = db.Column(db.Float)
    etalon = db.Column(db.Float)
    result = db.Column(db.Integer)
