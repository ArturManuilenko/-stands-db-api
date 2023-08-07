from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin


class Mail(db.Model, SerializerMixin):
    __tablename__ = 'mail'
    __table_args__ = {'schema': 'energomera'}
    id = db.Column(db.Integer, primary_key=True, unique=True)
    stend = db.Column(db.String(45))
    body = db.Column(db.String)
    delivered = db.Column(db.DateTime)
    from_ = db.Column('from', db.DateTime)
    to = db.Column(db.DateTime)
