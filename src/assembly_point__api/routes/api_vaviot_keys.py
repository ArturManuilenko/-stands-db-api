from api_utils.api_resource.api_resource import ApiResource
from api_utils.utils.constants import TJsonResponse

from src.conf.assembly_point__api import api_sdk

from src.assembly_point__db.helpers.get_vaviot_keys import get_vaviot_keys_list, get_vaviot_keys_list_total_count
import src.conf.permissions as permissions  # noqa: F401


@api_sdk.api_route_get('/vaviot-keys')
@api_sdk.rest_api(many=True, access=api_sdk.ACCESS_PUBLIC)
def sa_get_vaviot_keys_list(api_resource: ApiResource) -> TJsonResponse:
    vaviot_keys = get_vaviot_keys_list(
        limit=api_resource.pagination.limit,
        offset=api_resource.pagination.offset,
        filters=api_resource.filter_by.params,
        sorts=api_resource.sort_by.params
    )
    total_count = get_vaviot_keys_list_total_count(
        filters=api_resource.filter_by.params,
    )
    vaviot_keys_list = [vaviot_key.to_dict() for vaviot_key in vaviot_keys]
    return api_resource.response_list_ok(list_of_obj=vaviot_keys_list, total_count=total_count)
