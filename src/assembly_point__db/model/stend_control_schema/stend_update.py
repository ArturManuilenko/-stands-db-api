from db_utils import CustomQuery
from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin
from src.assembly_point__db.model.stend_control_schema.firm_files import FirmFiles
from src.assembly_point__db.model.stend_control_schema.stend_list import StendList


class StendUpdate(db.Model, SerializerMixin):
    __tablename__ = 'stend_update'
    __table_args__ = {'schema': 'stend_control_schema'}

    id = db.Column(db.Integer, primary_key=True, unique=True)
    file = db.Column(db.Integer, db.ForeignKey("stend_control_schema.firm_files.id"))
    file_model = db.relationship(
        FirmFiles,
        foreign_keys=[file],
        query_class=CustomQuery,
        uselist=False,
        lazy='joined'
    )
    stend = db.Column(db.Integer, db.ForeignKey("stend_control_schema.stend_list.stend_id"), unique=True)
    stend_model = db.relationship(
        StendList,
        foreign_keys=[stend],
        query_class=CustomQuery,
        uselist=False
    )
    enable = db.Column(db.Boolean)
    name = db.Column(db.String(45), unique=True)
