from api_utils.api_resource.api_resource import ApiResource
from api_utils.utils.constants import TJsonResponse

from src.conf.assembly_point__api import api_sdk

from src.assembly_point__db.helpers.get_measure import get_measure_list, get_measure_list_total_count
import src.conf.permissions as permissions  # noqa: F401


@api_sdk.api_route_get('/measure')
@api_sdk.rest_api(many=True, access=api_sdk.ACCESS_PUBLIC)
def sa_get_measures_list(api_resource: ApiResource) -> TJsonResponse:
    measures = get_measure_list(
        limit=api_resource.pagination.limit,
        offset=api_resource.pagination.offset,
        filters=api_resource.filter_by.params,
        sorts=api_resource.sort_by.params
    )
    total_count = get_measure_list_total_count(
        filters=api_resource.filter_by.params,
    )
    measure_list = [measure.to_dict() for measure in measures]
    return api_resource.response_list_ok(list_of_obj=measure_list, total_count=total_count)
