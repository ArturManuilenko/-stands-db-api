from db_utils import CustomQuery
from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin
from src.assembly_point__db.model.stend_control_schema.stend_list import StendList
from src.assembly_point__db.model.stend_control_schema.stend_groups import StendGroups


class StendGroupBind(db.Model, SerializerMixin):
    __tablename__ = 'stend_group_bind'
    __table_args__ = {'schema': 'stend_control_schema'}

    stend = db.Column(db.Integer, db.ForeignKey("stend_control_schema.stend_list.stend_id"))
    stend_model = db.relationship(
        StendList,
        foreign_keys=[stend],
        query_class=CustomQuery,
        uselist=False,
        lazy='joined'
    )
    group = db.Column(db.Integer, db.ForeignKey("stend_control_schema.stend_groups.id"))
    group_model = db.relationship(
        StendGroups,
        foreign_keys=[group],
        query_class=CustomQuery,
        uselist=False
    )
