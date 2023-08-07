from typing import Dict, Any, List
from db_utils.modules.db import db
from sqlalchemy import func

from src.assembly_point__db.model.calibration.stage_log_mysql import StageLogMySQL


def next_log_id() -> int:
    max_id = db.session.query(func.max(StageLogMySQL.id)).scalar()
    return max_id + 1


def add_log(stages: List[Dict[str, Any]], report) -> StageLogMySQL:
    for item in stages:
        number = item.get('number')
        name = item.get('name')
        log = item.get('log')
        result = item.get('result')
        new_log = StageLogMySQL(
            id=next_log_id(),
            report=report,
            number=number,  # TODO: validate fields report number name log result
            name=name,
            log=log,
            result=result,
        )
        db.session.add(new_log)
        db.session.commit()
        return new_log
