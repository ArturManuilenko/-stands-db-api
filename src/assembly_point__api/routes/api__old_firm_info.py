from typing import Dict, Any, Union, List
from pydantic import BaseModel

from src.assembly_point__db.helpers.get_stend_update import get_stend_update_by_id


class FirmInfoResponse(BaseModel):
    data: Dict[str, Union[List, str]]
    stand: int


def api_firm_info(data: Dict[str, Any]) -> Dict[str, Any]:
    stend = data['stend']
    cmd = data['data']['cmd']
    firm_info = get_stend_update_by_id(stend)
    data = {"info": [{
        "crc32": firm.file_model.crc32,
        "name": firm.name,
        "file_id": firm.file_model.id} for firm in firm_info],
        "cmd": cmd
    }
    result = FirmInfoResponse(data=data, stand=stend).dict()
    return result
