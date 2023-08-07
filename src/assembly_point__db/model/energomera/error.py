from db_utils import CustomQuery
from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin
from src.assembly_point__db.model.energomera.mail import Mail


class Error(db.Model, SerializerMixin):
    __tablename__ = 'error'
    __table_args__ = {'schema': 'energomera'}
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.Integer, db.ForeignKey("energomera.mail.id"))
    mail_model = db.relationship(
        Mail,
        foreign_keys=[mail],
        query_class=CustomQuery,
        uselist=False
    )
    line = db.Column(db.Integer(11))
    data = db.Column(db.DateTime)
    type = db.Column(db.Integer)
