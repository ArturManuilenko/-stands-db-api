import os

from api_utils.internal_api.internal_api import InternalApi

self_api = InternalApi(
    entry_point=os.environ['INTERNAL_API_ENDPOINT'],
    default_auth_token=os.environ['INTERNAL_JWT_ACCESS_TOKEN'],
)
