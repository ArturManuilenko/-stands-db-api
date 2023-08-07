from api_utils.api_resource.api_resource import ApiResource
from api_utils.utils.constants import TJsonResponse

from src.conf.assembly_point__api import api_sdk
from src.assembly_point__db.helpers.get_address_fluo import get_address_fluo_list, get_address_fluo_list_total_count
import src.conf.permissions as permissions  # noqa: F401


@api_sdk.api_route_get('/address-fluo')
@api_sdk.rest_api(many=True, access=api_sdk.ACCESS_PUBLIC)
def sa_get_address_fluo_list(api_resource: ApiResource) -> TJsonResponse:
    addresses_fluo = get_address_fluo_list(
        limit=api_resource.pagination.limit,
        offset=api_resource.pagination.offset,
        filters=api_resource.filter_by.params,
        sorts=api_resource.sort_by.params
    )
    total_count = get_address_fluo_list_total_count(
        filters=api_resource.filter_by.params,
    )
    address_fluo_list = [address_fluo.to_dict() for address_fluo in addresses_fluo]
    return api_resource.response_list_ok(list_of_obj=address_fluo_list, total_count=total_count)
