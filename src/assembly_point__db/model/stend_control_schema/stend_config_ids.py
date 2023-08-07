from db_utils.modules.db import db
from sqlalchemy_serializer import SerializerMixin


class StendConfigIds(db.Model, SerializerMixin):
    __tablename__ = 'stend_config_ids'
    __table_args__ = {'schema': 'stend_control_schema'}

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), unique=True)
    default = db.Column(db.String)
    description = db.Column(db.String)
