import math
from typing import Dict, Any, List
from db_utils.modules.db import db
from sqlalchemy import func

from src.assembly_point__db.model.calibration.measure_mysql import MeasureMySQL


def next_measure_id() -> int:
    max_id = db.session.query(func.max(MeasureMySQL.id)).scalar()
    return max_id + 1


def add_measure(measure_list: List[Dict[str, Any]], report) -> MeasureMySQL:
    for item in measure_list:
        error = item.get('error')
        value = item.get('value')
        etalon = item.get('etalon')
        if error is not None and (math.isinf(error) or math.isnan(error)):
            error = None
        if value is not None and (math.isinf(value) or math.isnan(value)):
            value = None
        if etalon is not None and (math.isinf(etalon) or math.isnan(etalon)):
            etalon = None
        if error is None and etalon is not None and etalon != 0.0 and value is not None:
            error = (value - etalon) / etalon * 100.0
        if value is None and etalon is not None and error is not None:
            value = etalon * (1.0 + error / 100.0)
        new_measure = MeasureMySQL(
            id=next_measure_id(),
            report=report,
            group=item['group'],  # TODO: validate fields group type phase result
            type=item['type'],
            phase=item['phase'],
            result=item['result'],
            error=error,
            value=value,
            etalon=etalon,
        )
        db.session.add(new_measure)
        db.session.commit()
        return new_measure
