from typing import Optional, List, Dict, Any, Tuple

from db_utils import db_search

from src.assembly_point__db.model.work.address_fluo_mysql import AddressFluoMySQL


def get_address_fluo_list(
    limit: Optional[int],
    offset: Optional[int],
    filters: List[Dict[str, Any]],
    sorts: List[Tuple[str, str]],
) -> List[AddressFluoMySQL]:

    address_fluo_list = db_search(
        model=AddressFluoMySQL,
        limit=limit,
        offset=offset,
        filters=filters,
        sorts=sorts
    ).all()
    return address_fluo_list


def get_address_fluo_list_total_count(
    filters: Optional[List[Dict[str, Any]]],
) -> int:
    address_fluo_list_count = db_search(
        model=AddressFluoMySQL,
        filters=filters
    ).count()
    return address_fluo_list_count
