from typing import Dict, Any, Union
from pydantic import BaseModel

from src.assembly_point__db.helpers.add_firm_upd_rep import add_new_firm_upd_rep


class FirmUpdRepResponse(BaseModel):
    data: Dict[str, Union[int, str]]
    stand: int


def api_firm_upd_rep(data: Dict[str, Any]) -> Dict[str, Any]:
    stand = data['stend']
    cmd = data['data']['cmd']
    name = data['data']['name']
    type = data['data']['type']
    md5 = data['data']['md5']
    version = data['data']['version']
    source = data['data']['source']
    descr = data['data']['comment']
    add_new_firm_upd_rep(stend=stand, name=name, type=type, md5=md5, version=version, source=source, descr=descr)
    data = {
        "cmd": cmd,
    }
    result = FirmUpdRepResponse(data=data, stand=stand).dict()
    return result
