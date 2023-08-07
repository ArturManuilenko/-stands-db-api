from api_utils.modules.api_sdk import ApiSdk
from api_utils.modules.api_sdk_config import ApiSdkConfig

from src.conf.permissions import permissions

api_sdk = ApiSdk(ApiSdkConfig(
    app_name=__name__,
    permissions=permissions,
))
