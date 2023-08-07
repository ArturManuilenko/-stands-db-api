from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin


class StendGroups(db.Model, SerializerMixin):
    __tablename__ = 'stend_groups'
    __table_args__ = {'schema': 'stend_control_schema'}

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(45), unique=True)
