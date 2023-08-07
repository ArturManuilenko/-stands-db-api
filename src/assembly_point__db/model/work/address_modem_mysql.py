from db_utils import CustomQuery
from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin

from src.assembly_point__db.model.work.chip_type_mysql import ChipTypeMySQL


class AddressModemMySQL(db.Model, SerializerMixin):
    __tablename__ = 'address_modem'
    __table_args__ = {'schema': 'work'}
    mac = db.Column(db.Integer)
    serial = db.Column(db.String(32), primary_key=True)
    chip_id = db.Column(db.Integer, db.ForeignKey("work.chip_type.id"))
    chip_model = db.relationship(
        ChipTypeMySQL,
        foreign_keys=[chip_id],
        query_class=CustomQuery,
        uselist=False,
        lazy='joined')
    datetime = db.Column(db.DateTime)
