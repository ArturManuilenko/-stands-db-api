from flask import Flask

from src.conf.assembly_point__api import api_sdk
from src.conf.assembly_point__db import db_config

flask_app: Flask = api_sdk.flask_app

db_config.attach_to_flask_app(flask_app)


__all__ = (
    'flask_app',
)
