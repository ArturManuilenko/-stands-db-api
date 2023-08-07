from typing import List, Any, Tuple, Dict
from typing import Optional


from db_utils.utils.search.search import db_search

from src.assembly_point__db.model.calibration.report_mysql import ReportMySQL


def get_report_list(
    limit: Optional[int],
    offset: Optional[int],
    filters: List[Dict[str, Any]],
    sorts: List[Tuple[str, str]],
) -> List[ReportMySQL]:
    report_result_query = ReportMySQL.query \
        .filter(ReportMySQL.result == "000-ok")
    report_list = db_search(
        initial_query=report_result_query,
        model=ReportMySQL,
        limit=limit,
        offset=offset,
        filters=filters,
        sorts=sorts
    ).all()
    return report_list


def get_report_list_total_count(
    filters: Optional[List[Dict[str, Any]]],
) -> int:
    report_list_count = db_search(
        model=ReportMySQL,
        filters=filters
    ).count()
    return report_list_count
