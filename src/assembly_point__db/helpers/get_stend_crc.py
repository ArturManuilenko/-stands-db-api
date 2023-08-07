from typing import List, Any, Tuple, Dict
from typing import Optional

from db_utils.utils.search.search import db_search

from src.assembly_point__db.model.stend_control_schema.stend_crc import StendCrc


def get_stend_crc_list(
    limit: Optional[int],
    offset: Optional[int],
    filters: List[Dict[str, Any]],
    sorts: List[Tuple[str, str]],
) -> List[StendCrc]:
    stend_crc_list = db_search(
        model=StendCrc,
        limit=limit,
        offset=offset,
        filters=filters,
        sorts=sorts
    ).all()
    return stend_crc_list


def get_stend_crc_list_total_count(
    filters: Optional[List[Dict[str, Any]]],
) -> int:
    stend_crc_list_count = db_search(
        model=StendCrc,
        filters=filters
    ).count()
    return stend_crc_list_count
