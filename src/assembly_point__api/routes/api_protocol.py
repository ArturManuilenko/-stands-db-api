from api_utils.api_resource.api_resource import ApiResource
from api_utils.utils.constants import TJsonResponse

from src.conf.assembly_point__api import api_sdk

from src.assembly_point__db.helpers.get_protocol import get_protocol_list, get_protocol_list_total_count
import src.conf.permissions as permissions  # noqa: F401


@api_sdk.api_route_get('/protocol')
@api_sdk.rest_api(many=True, access=api_sdk.ACCESS_PUBLIC)
def sa_get_protocols_list(api_resource: ApiResource) -> TJsonResponse:
    protocols = get_protocol_list(
        limit=api_resource.pagination.limit,
        offset=api_resource.pagination.offset,
        filters=api_resource.filter_by.params,
        sorts=api_resource.sort_by.params
    )
    total_count = get_protocol_list_total_count(
        filters=api_resource.filter_by.params,
    )
    protocol_list = [protocol.to_dict() for protocol in protocols]
    return api_resource.response_list_ok(list_of_obj=protocol_list, total_count=total_count)
