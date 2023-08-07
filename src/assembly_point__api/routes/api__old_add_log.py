from typing import Dict, Any, Union
from pydantic import BaseModel

from src.assembly_point__db.helpers.add_log import add_log


class LogResponse(BaseModel):
    data: Dict[str, Union[int, str]]
    stand: int


def api_add_log(data: Dict[str, Any]) -> Dict[str, Any]:
    stand = data['stend']
    cmd = data['data']['cmd']
    report = data['data']['report']
    stages = data['data']['stages']
    add_log(stages=stages, report=report)
    data = {
        "cmd": cmd
    }
    result = LogResponse(data=data, stand=stand).dict()
    return result
