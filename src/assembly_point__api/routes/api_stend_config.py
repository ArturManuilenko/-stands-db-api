from api_utils.api_resource.api_resource import ApiResource
from api_utils.utils.constants import TJsonResponse

from src.conf.assembly_point__api import api_sdk

from src.assembly_point__db.helpers.get_stend_config import get_stend_config_list, get_stend_config_list_total_count
import src.conf.permissions as permissions  # noqa: F401


@api_sdk.api_route_get('/stend-config')
@api_sdk.rest_api(many=True, access=api_sdk.ACCESS_PUBLIC)
def sa_get_stend_configs_list(api_resource: ApiResource) -> TJsonResponse:
    stend_configs = get_stend_config_list(
        limit=api_resource.pagination.limit,
        offset=api_resource.pagination.offset,
        filters=api_resource.filter_by.params,
        sorts=api_resource.sort_by.params
    )
    total_count = get_stend_config_list_total_count(
        filters=api_resource.filter_by.params,
    )
    stend_config_list = [stend_config.to_dict() for stend_config in stend_configs]
    return api_resource.response_list_ok(list_of_obj=stend_config_list, total_count=total_count)
