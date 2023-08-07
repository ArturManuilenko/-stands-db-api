from typing import Tuple

from api_utils.api_resource.api_resource import ApiResource
from flask import render_template

from src.conf.assembly_point__web import web_sdk


@web_sdk.api_route_get('/')
@web_sdk.html_view(many=False, access=web_sdk.ACCESS_PUBLIC)
def view_list_logs(api_resource: ApiResource) -> Tuple[str, int]:
    return render_template(
        'index.html',
        active="list_logs",
        title='Logs',
        data={},
        pagination=api_resource.pagination.mk_sqlalchemy_pagination(query=None, total=0, items=[]),
    ), 200
