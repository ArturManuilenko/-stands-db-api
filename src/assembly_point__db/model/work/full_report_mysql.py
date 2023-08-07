from db_utils import CustomQuery
from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin

from src.assembly_point__db.model.work.test_descr_mysql import TestDescrMySQL


class FullReportMySQL(db.Model, SerializerMixin):
    __tablename__ = 'full_report'
    __table_args__ = {'schema': 'work'}
    test_id = db.Column(db.Integer, db.ForeignKey("work.test_descr.id"))
    test_model = db.relationship(
        TestDescrMySQL,
        foreign_keys=[test_id],
        query_class=CustomQuery,
        uselist=False,
        lazy='joined'
    )
    string = db.Column(db.String, primary_key=True)
