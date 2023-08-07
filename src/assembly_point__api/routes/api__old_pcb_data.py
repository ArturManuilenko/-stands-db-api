from typing import Dict, Any, Union
from pydantic import BaseModel

from src.assembly_point__db.helpers.get_pcb_type import get_pcb_type_by_id


class PCBTypeResponse(BaseModel):
    data: Dict[str, Union[int, str]]
    stand: int


def api_pcb_type(data: Dict[str, Any]) -> Dict[str, Any]:
    stand = data['stend']
    cmd = data['data']['cmd']
    pcb_id = data['data']['id']
    pcb = get_pcb_type_by_id(pcb_id)
    if pcb is None:
        data = {
            "data": "",
            "device": "-",
            "cmd": cmd,
            "modification": "-"
        }
    else:
        response = pcb.to_dict()
        if response['data'] is None:
            data = {
                "data": "",
                "device": response['model'],
                "cmd": cmd,
                "modification": response['modification']
            }
    result = PCBTypeResponse(data=data, stand=stand).dict()
    return result
