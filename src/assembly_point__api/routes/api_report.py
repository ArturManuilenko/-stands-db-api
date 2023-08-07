from typing import Tuple

from api_utils.api_resource.api_resource import ApiResource
from api_utils.utils.constants import TJsonResponse

from src.conf.assembly_point__api import api_sdk

from src.assembly_point__db.helpers.get_report import get_report_list, get_report_list_total_count
import src.conf.permissions as permissions  # noqa: F401


get_object_list__report_serialize_rules: Tuple[str, ...] = (
    '-launch_model.unit',
    '-launch_model.unit_info',
    '-launch_model.unit_model',
    '-launch_model.unit_info_model',
)


@api_sdk.api_route_get('/report/result_ok')
@api_sdk.rest_api(many=True, access=api_sdk.ACCESS_PUBLIC)
def sa_get_report_result_ok_list(api_resource: ApiResource) -> TJsonResponse:
    reports = get_report_list(
        limit=api_resource.pagination.limit,
        offset=api_resource.pagination.offset,
        filters=api_resource.filter_by.params,
        sorts=api_resource.sort_by.params
    )
    total_count = get_report_list_total_count(
        filters=api_resource.filter_by.params,
    )
    report_list = [report.to_dict(rules=get_object_list__report_serialize_rules) for report in reports]
    return api_resource.response_list_ok(list_of_obj=report_list, total_count=total_count)
