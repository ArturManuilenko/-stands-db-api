from db_utils import CustomQuery
from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin
from src.assembly_point__db.model.energomera.mail import Mail


class Firm(db.Model, SerializerMixin):
    __tablename__ = 'firm'
    __table_args__ = {'schema': 'energomera'}
    id = db.Column(db.Integer, primary_key=True, unique=True)
    mail = db.Column(db.Integer, db.ForeignKey("energomera.mail.id"))
    mail_model = db.relationship(
        Mail,
        foreign_keys=[mail],
        query_class=CustomQuery,
        uselist=False,
        lazy='joined'
    )
    line = db.Column(db.Integer)
    data = db.Column(db.DateTime)
    mac = db.Column(db.Integer)
    serial = db.Column(db.String(45))
    version = db.Column(db.String(45))
    rep = db.Column(db.Integer)
    result = db.Column(db.Integer)
    new = db.Column(db.Integer)
