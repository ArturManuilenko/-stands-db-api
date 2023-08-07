from typing import Optional, List, Dict, Any, Tuple

from db_utils.utils.search.search import db_search

from src.assembly_point__db.model.work.vaviot_keys_mysql import VaviotKeysMySQL


def get_vaviot_keys_list(
    limit: Optional[int],
    offset: Optional[int],
    filters: List[Dict[str, Any]],
    sorts: List[Tuple[str, str]],
) -> List[VaviotKeysMySQL]:

    vaviot_keys_list = db_search(
        model=VaviotKeysMySQL,
        limit=limit,
        offset=offset,
        filters=filters,
        sorts=sorts
    ).all()
    return vaviot_keys_list


def get_vaviot_keys_list_total_count(
    filters: Optional[List[Dict[str, Any]]],
) -> int:
    vaviot_keys_list_count = db_search(
        model=VaviotKeysMySQL,
        filters=filters
    ).count()
    return vaviot_keys_list_count
