from db_utils import CustomQuery
from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin

from src.assembly_point__db.model.calibration.unit_info_mysql import UnitInfoMySQL


class UnitMySQL(db.Model, SerializerMixin):
    __tablename__ = 'unit'
    __table_args__ = {'schema': 'calibration'}
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String, db.ForeignKey("calibration.unit_info.id"))
    info_model = db.relationship(
        UnitInfoMySQL,
        foreign_keys=[info],
        query_class=CustomQuery,
        uselist=False,
        lazy='joined')
    name = db.Column(db.String(45))
