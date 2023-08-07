from typing import List, Any, Tuple, Dict
from typing import Optional


from db_utils.utils.search.search import db_search

from src.assembly_point__db.model.energomera.mail import Mail


def get_mail_list(
    limit: Optional[int],
    offset: Optional[int],
    filters: List[Dict[str, Any]],
    sorts: List[Tuple[str, str]],
) -> List[Mail]:
    mail_list = db_search(
        model=Mail,
        limit=limit,
        offset=offset,
        filters=filters,
        sorts=sorts
    ).all()
    return mail_list


def get_mail_list_total_count(
    filters: Optional[List[Dict[str, Any]]],
) -> int:
    mail_list_count = db_search(
        model=Mail,
        filters=filters
    ).count()
    return mail_list_count
