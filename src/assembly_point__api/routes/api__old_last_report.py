from typing import Dict, Any, Union
from pydantic import BaseModel

from src.assembly_point__db.helpers.get_last_report import get_last_report_by_mac


class LastReportResponse(BaseModel):
    data: Dict[str, Union[int, str]]
    stand: int


def api_last_report(data: Dict[str, Any]) -> Dict[str, Any]:
    stend = data['stend']
    cmd = data['data']['cmd']
    mac = data['data']['mac']
    result = get_last_report_by_mac(mac).to_dict()
    data = {
        "report_id": result['id'],
        "cmd": cmd,
    }
    result = LastReportResponse(data=data, stand=stend).dict()
    return result
