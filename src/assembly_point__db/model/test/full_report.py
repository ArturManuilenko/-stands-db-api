from db_utils import CustomQuery
from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin
from src.assembly_point__db.model.test.test_descr import TestDescr


class FullReport(db.Model, SerializerMixin):
    __tablename__ = 'full_report'
    __table_args__ = {'schema': 'test'}

    test_id = db.Column(db.Integer, db.ForeignKey("test.test_descr.id"))
    test_id_model = db.relationship(
        TestDescr,
        foreign_keys=[test_id],
        query_class=CustomQuery,
        uselist=False
    )
    string = db.Column(db.String)
