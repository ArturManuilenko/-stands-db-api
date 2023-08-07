from flask import Flask

from src.conf.assembly_point__web import web_sdk

flask_app: Flask = web_sdk.flask_app

web_sdk.load_routes()

__all__ = (
    'flask_app',
)
