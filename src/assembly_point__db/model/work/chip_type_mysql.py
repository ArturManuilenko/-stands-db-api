from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin


class ChipTypeMySQL(db.Model, SerializerMixin):
    __tablename__ = 'chip_type'
    __table_args__ = {'schema': 'work'}
    id = db.Column(db.Integer, primary_key=True)
    descr = db.Column(db.String)
