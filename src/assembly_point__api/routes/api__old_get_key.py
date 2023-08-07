from typing import Dict, Any, Union

from pydantic import BaseModel

from src.assembly_point__db.helpers.get_stend_list import get_stend_by_id
from src.assembly_point__db.helpers.table_name_model_map import TABLE_NAME_TO_MODEL__MAP


class GetKeyResponse(BaseModel):
    data: Dict[str, Union[int, str]]
    stand: int


def api_get_key(data: Dict[str, Any]) -> Dict[str, Any]:
    stend = data['stend']
    cmd = data['data']['cmd']
    mac = data['data']['mac']
    stand = get_stend_by_id(stend).to_dict()
    table = stand['device_model']['pool_table']
    model = TABLE_NAME_TO_MODEL__MAP[table]
    result = model.query.filter_by(mac=mac).first()
    response = result.to_dict()
    data = {
        "mac": response['mac'],
        "cmd": cmd,
        "key": response['key']
    }
    result = GetKeyResponse(data=data, stand=stend).dict()
    return result
