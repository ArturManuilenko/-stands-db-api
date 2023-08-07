from db_utils import CustomQuery
from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin

from src.assembly_point__db.model.calibration.algoritm_mysql import AlgoritmMySQL
from src.assembly_point__db.model.calibration.unit_info_mysql import UnitInfoMySQL
from src.assembly_point__db.model.calibration.unit_mysql import UnitMySQL


class LaunchMySQL(db.Model, SerializerMixin):
    __tablename__ = 'launch'
    __table_args__ = {'schema': 'calibration'}
    id = db.Column(db.Integer, primary_key=True)
    algoritm = db.Column(db.Integer, db.ForeignKey("calibration.algoritm.id"))
    algoritm_model = db.relationship(
        AlgoritmMySQL,
        foreign_keys=[algoritm],
        query_class=CustomQuery,
        uselist=False,
        lazy='joined')
    unit = db.Column(db.Integer, db.ForeignKey("calibration.unit.id"))
    unit_model = db.relationship(
        UnitMySQL,
        foreign_keys=[unit],
        query_class=CustomQuery,
        uselist=False,
        lazy='joined')
    unit_info = db.Column(db.Integer, db.ForeignKey("calibration.unit_info.id"))
    unit_info_model = db.relationship(
        UnitInfoMySQL,
        foreign_keys=[unit_info],
        query_class=CustomQuery,
        uselist=False,
        lazy='joined')
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    stage_count = db.Column(db.Integer)
