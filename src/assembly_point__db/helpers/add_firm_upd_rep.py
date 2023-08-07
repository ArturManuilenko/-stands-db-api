from datetime import datetime

from db_utils.modules.db import db
from sqlalchemy import func

from src.assembly_point__db.model.work.log_update_mysql import LogUpdateMySQL


def next_id() -> int:
    max_id = db.session.query(func.max(LogUpdateMySQL.id)).scalar()
    return max_id + 1


def add_new_firm_upd_rep(
    name: str,
    type: str,
    md5: str,
    version: str,
    source: str,
    descr: str,
    stend: int,
) -> LogUpdateMySQL:
    new_log_update = LogUpdateMySQL(
        id=next_id(),
        stend=stend,
        name=name,
        type=type,
        md5=md5,
        version=version,
        source=source,
        descr=descr,
        time=datetime.now()
    )
    db.session.add(new_log_update)
    db.session.commit()
    return new_log_update

