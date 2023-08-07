from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin


class Installment(db.Model, SerializerMixin):
    __tablename__ = 'installment'
    __table_args__ = {'schema': 'smarthome'}
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(45), unique=True)
    description = db.Column(db.String)
    model = db.Column(db.Integer)
    modification = db.Column(db.String(45))
    time = db.Column(db.DateTime)
    open = db.Column(db.Boolean)
    mode = db.Column(db.Integer)
