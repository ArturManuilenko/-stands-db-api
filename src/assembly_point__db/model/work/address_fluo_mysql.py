from db_utils import CustomQuery
from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin

from src.assembly_point__db.model.work.chip_type_mysql import ChipTypeMySQL
from src.assembly_point__db.model.work.vaviot_keys_mysql import VaviotKeysMySQL


class AddressFluoMySQL(db.Model, SerializerMixin):
    __tablename__ = 'address_fluo'
    __table_args__ = {'schema': 'work'}

    mac = db.Column(db.Integer, db.ForeignKey("work.vaviot_keys.mac"))
    mac_model = db.relationship(VaviotKeysMySQL,
                                foreign_keys=[mac],
                                query_class=CustomQuery,
                                uselist=False,
                                lazy='joined')
    chip_id = db.Column(db.Integer, db.ForeignKey("work.chip_type.id"))
    chip_model = db.relationship(ChipTypeMySQL,
                                 foreign_keys=[chip_id],
                                 query_class=CustomQuery,
                                 uselist=False,
                                 lazy='joined')
    serial = db.Column(db.String(32), primary_key=True)
    datetime = db.Column(db.DateTime)
