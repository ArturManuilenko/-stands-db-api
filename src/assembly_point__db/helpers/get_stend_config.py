from typing import List, Any, Tuple, Dict
from typing import Optional

from db_utils.utils.search.search import db_search

from src.assembly_point__db.model.stend_control_schema.stend_config import StendConfig


def get_stend_config_list(
    limit: Optional[int],
    offset: Optional[int],
    filters: List[Dict[str, Any]],
    sorts: List[Tuple[str, str]],
) -> List[StendConfig]:
    stend_config_list = db_search(
        model=StendConfig,
        limit=limit,
        offset=offset,
        filters=filters,
        sorts=sorts
    ).all()
    return stend_config_list


def get_stend_config_list_total_count(
    filters: Optional[List[Dict[str, Any]]],
) -> int:
    stend_config_list_count = db_search(
        model=StendConfig,
        filters=filters
    ).count()
    return stend_config_list_count
