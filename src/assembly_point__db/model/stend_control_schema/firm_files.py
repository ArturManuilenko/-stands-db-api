from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin


class FirmFiles(db.Model, SerializerMixin):
    __tablename__ = 'firm_files'
    __table_args__ = {'schema': 'stend_control_schema'}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    type = db.Column(db.String(32))
    md5 = db.Column(db.String(32), unique=True)
    crc32 = db.Column(db.String(32))
    data = db.Column(db.LargeBinary)
    time = db.Column(db.DateTime)
    version = db.Column(db.String(45))
    repository = db.Column(db.String)
    comment = db.Column(db.String)
