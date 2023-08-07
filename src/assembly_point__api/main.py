from src.conf.assembly_point__api import api_sdk
from src.assembly_point__api.flask import flask_app

api_sdk.load_routes()

__all__ = (
    'flask_app',
)
