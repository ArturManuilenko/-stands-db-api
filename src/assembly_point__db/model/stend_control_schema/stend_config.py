from db_utils import CustomQuery
from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin
from src.assembly_point__db.model.stend_control_schema.stend_list import StendList
from src.assembly_point__db.model.stend_control_schema.stend_config_ids import StendConfigIds


class StendConfig(db.Model, SerializerMixin):
    __tablename__ = 'stend_config'
    __table_args__ = {'schema': 'stend_control_schema'}

    id = db.Column(db.Integer, primary_key=True)

    stend = db.Column(db.Integer, db.ForeignKey("stend_control_schema.stend_list.stend_id"))
    stend_model = db.relationship(
        StendList,
        foreign_keys=[stend],
        query_class=CustomQuery,
        uselist=False,
        lazy='joined'
    )
    config = db.Column(db.Integer, db.ForeignKey("stend_control_schema.stend_config_ids.id"))
    config_model = db.relationship(
        StendConfigIds,
        foreign_keys=[config],
        query_class=CustomQuery,
        uselist=False,
        lazy='joined'
    )
    value = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
