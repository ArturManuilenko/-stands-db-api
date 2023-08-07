from db_utils import CustomQuery
from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin

from src.assembly_point__db.model.work.chip_type_mysql import ChipTypeMySQL
from src.assembly_point__db.model.work.lora_keys_mysql import LoraKeysMySQL


class AddressloraMySQL(db.Model, SerializerMixin):
    __tablename__ = 'address_lora'
    __table_args__ = {'schema': 'work'}
    mac = db.Column(db.BigInteger, db.ForeignKey("work.lora_keys.mac"))
    mac_model = db.relationship(
        LoraKeysMySQL,
        foreign_keys=[mac],
        query_class=CustomQuery,
        uselist=False,
        lazy='joined')
    serial = db.Column(db.String(32), primary_key=True)
    chip_id = db.Column(db.Integer, db.ForeignKey("work.chip_type.id"))
    chip_model = db.relationship(
        ChipTypeMySQL,
        foreign_keys=[chip_id],
        query_class=CustomQuery,
        uselist=False,
        lazy='joined')
    datetime = db.Column(db.DateTime)
