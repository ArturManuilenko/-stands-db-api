from typing import Dict, Any, Union
from pydantic import BaseModel

from src.assembly_point__db.helpers.get_stend_list import get_stend_by_id


class InfoResponse(BaseModel):
    data: Dict[str, Union[int, str]]
    stand: int


def api_info(data: Dict[str, Any]) -> Dict[str, Any]:
    stend = data['stend']
    cmd = data['data']['cmd']
    result = get_stend_by_id(stend)
    response = result.to_dict()
    data = {
        "mac_gen": response['generate'],
        "mac_class": response['device_model']['name'],
        "cmd": cmd,
        "descr": response['description']
    }
    stand = response['stend_id']
    result = InfoResponse(data=data, stand=stand).dict()
    return result
