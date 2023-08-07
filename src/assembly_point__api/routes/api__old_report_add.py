from typing import Dict, Any, Union
from pydantic import BaseModel

from src.assembly_point__db.helpers.add_full_report import add_full_report
from src.assembly_point__db.helpers.add_test_descr import add_new_test_descr, last_test_descr_id


class ReportAddResponse(BaseModel):
    data: Dict[str, Union[int, str]]
    stand: int


def api_report_add(data: Dict[str, Any]) -> Dict[str, Any]:
    stand = data['stend']
    cmd = data['data']['cmd']
    start = data['data']['start']
    serial = data['data']['serial']
    mac = data['data']['mac']
    errors = data['data']['errors']
    text = data['data']['text']
    add_new_test_descr(start=start, serial=serial, mac=mac, errors=errors, stend_id=stand)
    add_full_report(string=text)
    data = {
        "test_id": last_test_descr_id(),
        "cmd": cmd
    }
    result = ReportAddResponse(data=data, stand=stand).dict()
    return result
