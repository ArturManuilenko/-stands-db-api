from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin


class OutUpdate(db.Model, SerializerMixin):
    __tablename__ = 'out_update'
    __table_args__ = {'schema': 'stend_control_schema'}

    path = db.Column(db.Integer, primary_key=True, unique=True)
    md5 = db.Column(db.String(32))
    data = db.Column(db.LargeBinary)
    time = db.Column(db.DateTime)
    version = db.Column(db.String(45))
    repository = db.Column(db.String)
