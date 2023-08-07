from api_utils.modules.api_sdk import ApiSdk
from api_utils.modules.api_sdk_config import ApiSdkConfig

from src.conf.permissions import permissions


web_sdk = ApiSdk(ApiSdkConfig(
    app_name=__name__,
    permissions=permissions,
    default_max_limit=20,
    check_access=False,
    check_environment=False,
    api_route_path_prefix='',
))
