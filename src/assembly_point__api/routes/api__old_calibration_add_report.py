from typing import Dict, Any, Union
from pydantic import BaseModel

from src.assembly_point__db.helpers.add_calibration_report import add_report, last_report_id


class AddReportResponse(BaseModel):
    data: Dict[str, Union[int, str]]
    stand: int


def api_calibration_add_report(data: Dict[str, Any]) -> Dict[str, Any]:
    stand = data['stend']
    cmd = data['data']['cmd']
    launch = data['data']['launch']
    place = data['data']['place']
    mac = data['data']['mac']
    result = data['data']['result']
    add_report(launch=launch, place=place, mac=mac, result=result)
    data = {
        "cmd": cmd,
        "report_id": last_report_id()
    }
    result = AddReportResponse(data=data, stand=stand).dict()
    return result
