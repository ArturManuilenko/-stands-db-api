from db_utils import attach_to_flask_app
from db_utils.modules.db import db
from flask import Flask
from flask_migrate import Migrate

from src.conf.assembly_point__db import db_config
import src.assembly_point__db.model.models as models

db_flask_app = Flask(__name__)

attach_to_flask_app(db_flask_app, db_config)

migrate = Migrate(compare_type=True)
migrate.init_app(db_flask_app, db)


__all__ = (
    'models',
    'db_flask_app',
)
