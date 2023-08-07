from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin


class ProtocolReportsMySQL(db.Model, SerializerMixin):
    __tablename__ = 'protocol_reports'
    id = db.Column(db.Integer, primary_key=True)
    report = db.Column(db.Integer, db.ForeignKey("calibration.report.id"))
    protocol = db.Column(db.Integer, db.ForeignKey("calibration.protocol.id"))
