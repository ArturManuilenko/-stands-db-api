from typing import List, Any, Tuple, Dict
from typing import Optional


from db_utils.utils.search.search import db_search

from src.assembly_point__db.model.calibration.protocol_mysql import ProtocolMySQL


def get_protocol_list(
    limit: Optional[int],
    offset: Optional[int],
    filters: List[Dict[str, Any]],
    sorts: List[Tuple[str, str]],
) -> List[ProtocolMySQL]:
    protocol_list = db_search(
        model=ProtocolMySQL,
        limit=limit,
        offset=offset,
        filters=filters,
        sorts=sorts
    ).all()
    return protocol_list


def get_protocol_list_total_count(
    filters: Optional[List[Dict[str, Any]]],
) -> int:
    protocol_list_count = db_search(
        model=ProtocolMySQL,
        filters=filters
    ).count()
    return protocol_list_count
