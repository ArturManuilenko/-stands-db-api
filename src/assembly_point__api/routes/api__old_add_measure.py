from typing import Dict, Any, Union
from pydantic import BaseModel

from src.assembly_point__db.helpers.add_measure import add_measure


class MeasureResponse(BaseModel):
    data: Dict[str, Union[int, str]]
    stand: int


def api_add_measure(data: Dict[str, Any]) -> Dict[str, Any]:
    stand = data['stend']
    cmd = data['data']['cmd']
    report = data['data']['report']
    measures = data['data']['measures']
    add_measure(measure_list=measures, report=report)
    data = {
        "cmd": cmd
    }
    result = MeasureResponse(data=data, stand=stand).dict()
    return result
