from db_utils.modules.db import db
from sqlalchemy import func

from src.assembly_point__db.model.calibration.report_mysql import ReportMySQL


def next_report_id() -> int:
    max_id = db.session.query(func.max(ReportMySQL.id)).scalar()
    return max_id + 1


def last_report_id() -> int:
    max_id = db.session.query(func.max(ReportMySQL.id)).scalar()
    return max_id


def add_report(
    launch: int,
    place: int,
    mac: int,
    result: int,
) -> ReportMySQL:
    new_report = ReportMySQL(
        id=next_report_id(),
        launch=launch,
        place=place,           # TODO: validate fields
        mac=mac,
        result=result,
        serial=None,
        factory=None,
    )
    db.session.add(new_report)
    db.session.commit()
    return new_report
