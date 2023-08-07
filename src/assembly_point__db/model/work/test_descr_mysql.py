from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin


class TestDescrMySQL(db.Model, SerializerMixin):
    __tablename__ = 'test_descr'
    __table_args__ = {'schema': 'work'}
    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String(32))
    mac = db.Column(db.Integer)
    stend_id = db.Column(db.Integer)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    errors = db.Column(db.Integer)
