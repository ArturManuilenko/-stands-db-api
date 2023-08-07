from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin


class ModificationList(db.Model, SerializerMixin):
    __tablename__ = 'modification_list'
    __table_args__ = {'schema': 'stend_control_schema'}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True)
    model = db.Column(db.String(45))
    description = db.Column(db.String(255))
