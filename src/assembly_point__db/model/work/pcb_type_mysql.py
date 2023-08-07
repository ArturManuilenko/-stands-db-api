from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin


class PCBTypeMySQL(db.Model, SerializerMixin):
    __tablename__ = 'pcb_type'
    __table_args__ = {'schema': 'work'}
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(255))
    modification = db.Column(db.String(255))
    data = db.Column(db.LargeBinary)
