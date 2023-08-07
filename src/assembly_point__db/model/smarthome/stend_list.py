from db_utils import CustomQuery
from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin
from src.assembly_point__db.model.smarthome.installment import Installment


class StendList(db.Model, SerializerMixin):
    __tablename__ = 'stend_list'
    __table_args__ = {'schema': 'smarthome'}
    id = db.Column(db.Integer, primary_key=True, unique=True)
    installment = db.Column(db.Integer, db.ForeignKey("smarthome.installment.id"))
    installment_model = db.relationship(
        Installment,
        foreign_keys=[installment],
        query_class=CustomQuery,
        uselist=False,
        lazy='joined'
    )
    description = db.Column(db.String)
