from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin


class WebAccess(db.Model, SerializerMixin):
    __tablename__ = 'web_access'
    __table_args__ = {'schema': 'web'}
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(45))
    passhash = db.Column(db.String(32))
    token = db.Column(db.String(512))
    admin = db.Column(db.Integer)
    protocol = db.Column(db.Integer)
    edit_protocol = db.Column(db.Integer)
