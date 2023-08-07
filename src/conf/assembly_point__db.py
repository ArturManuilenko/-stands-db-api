import os

from db_utils import DbConfig


db_config = DbConfig(
    uri=os.environ['ASSEMBLY_POINT__DB_URI'],
)
