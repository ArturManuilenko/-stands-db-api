from typing import List, Any, Tuple, Dict
from typing import Optional


from db_utils.utils.search.search import db_search

from src.assembly_point__db.model.calibration.measure_mysql import MeasureMySQL


def get_measure_list(
    limit: Optional[int],
    offset: Optional[int],
    filters: List[Dict[str, Any]],
    sorts: List[Tuple[str, str]],
) -> List[MeasureMySQL]:
    measure_list = db_search(
        model=MeasureMySQL,
        limit=limit,
        offset=offset,
        filters=filters,
        sorts=sorts
    ).all()
    return measure_list


def get_measure_list_total_count(
    filters: Optional[List[Dict[str, Any]]],
) -> int:
    measure_list_count = db_search(
        model=MeasureMySQL,
        filters=filters
    ).count()
    return measure_list_count
