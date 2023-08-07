from db_utils import CustomQuery
from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin

from src.assembly_point__db.model.calibration.launch_mysql import LaunchMySQL


class ReportMySQL(db.Model, SerializerMixin):
    __tablename__ = 'report'
    __table_args__ = {'schema': 'calibration'}
    id = db.Column(db.Integer, primary_key=True)
    launch = db.Column(db.Integer, db.ForeignKey("calibration.launch.id"))
    launch_model = db.relationship(
        LaunchMySQL,
        foreign_keys=[launch],
        query_class=CustomQuery,
        uselist=False,
        lazy='joined')
    place = db.Column(db.Integer)
    mac = db.Column(db.Integer)
    serial = db.Column(db.String(32))
    factory = db.Column(db.String(45))
    result = db.Column(db.String(20))
