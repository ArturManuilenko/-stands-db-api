from db_utils import CustomQuery
from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin

from src.assembly_point__db.model.work.pcb_type_mysql import PCBTypeMySQL


class PCBIdMySQL(db.Model, SerializerMixin):
    __tablename__ = 'pcb_id'
    __table_args__ = {'schema': 'work'}
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(45))
    type = db.Column(db.Integer, db.ForeignKey("work.pcb_type.id"))
    type_model = db.relationship(
        PCBTypeMySQL,
        foreign_keys=[id],
        query_class=CustomQuery,
        uselist=False,
        lazy='joined'
    )