from db_utils.modules.db import db
from sqlalchemy import func

from src.assembly_point__db.model.work.full_report_mysql import FullReportMySQL


def next_full_report_id() -> int:
    max_id = db.session.query(func.max(FullReportMySQL.test_id)).scalar()
    return max_id + 1


def add_full_report(
    string: str,
) -> FullReportMySQL:
    new_full_report = FullReportMySQL(
        string=string,
        test_id=next_full_report_id()
    )
    db.session.add(new_full_report)
    db.session.commit()
    return new_full_report
