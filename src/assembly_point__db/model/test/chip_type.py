from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin


class ChipType(db.Model, SerializerMixin):
    __tablename__ = 'chip_type'
    __table_args__ = {'schema': 'test'}
    id = db.Column(db.Integer, primary_key=True, unique=True)
    descr = db.Column(db.String(45), unique=True)
