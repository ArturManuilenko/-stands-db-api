import os

from sqlalchemy.engine.url import make_url

STANDS_DB__URI = os.environ['ASSEMBLY_POINT__DB_URI']
parsed_url = make_url(STANDS_DB__URI)
DB_USER = parsed_url.username
DB_PASS = parsed_url.password
DB_HOST = parsed_url.host
DB_PORT = parsed_url.port
DB_CONFIG = {
    'user': DB_USER,
    'password': DB_PASS,
    'host': DB_HOST,
    'port': DB_PORT
}
