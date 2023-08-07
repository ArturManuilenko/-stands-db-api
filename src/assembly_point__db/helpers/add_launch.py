from datetime import datetime

from db_utils.modules.db import db
from sqlalchemy import func

from src.assembly_point__db.model.calibration.launch_mysql import LaunchMySQL


def last_launch_id() -> int:
    max_id = db.session.query(func.max(LaunchMySQL.id)).scalar()
    return max_id


def next_launch_id() -> int:
    max_id = db.session.query(func.max(LaunchMySQL.id)).scalar()
    return max_id + 1


def add_launch(
    algoritm: int,
    unit_info: int,
    unit: int,
    start: datetime,
    end: datetime,
    stage_count: int
) -> LaunchMySQL:
    new_launch = LaunchMySQL(
        id=next_launch_id(),
        algoritm=algoritm,
        unit_info=unit_info,
        unit=unit,
        start=start,
        end=end,
        stage_count=stage_count
    )
    db.session.add(new_launch)
    db.session.commit()
    return new_launch
