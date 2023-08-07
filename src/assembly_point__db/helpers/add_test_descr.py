from datetime import datetime
from db_utils.modules.db import db
from sqlalchemy import func

from src.assembly_point__db.model.work.test_descr_mysql import TestDescrMySQL


def next_test_descr_id() -> int:
    max_id = db.session.query(func.max(TestDescrMySQL.id)).scalar()
    return max_id + 1


def last_test_descr_id() -> int:
    max_id = db.session.query(func.max(TestDescrMySQL.id)).scalar()
    return max_id


def add_new_test_descr(
    start: datetime,
    serial: str,
    mac: int,
    errors: int,
    stend_id: int
) -> TestDescrMySQL:
    new_test_descr = TestDescrMySQL(
        id=next_test_descr_id(),
        serial=serial,
        mac=mac,
        stend_id=stend_id,
        start=start,
        end=datetime.now(),
        errors=errors,
    )
    db.session.add(new_test_descr)
    db.session.commit()
    return new_test_descr
