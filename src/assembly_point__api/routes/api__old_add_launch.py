from typing import Dict, Any, Union
from pydantic import BaseModel

from src.assembly_point__db.helpers.add_calibration_report import add_report, next_report_id
from src.assembly_point__db.helpers.add_launch import add_launch, last_launch_id
from src.assembly_point__db.helpers.add_log import add_log
from src.assembly_point__db.helpers.add_measure import add_measure
from src.assembly_point__db.helpers.get_algoritm_id_by_name import get_algoritm_id_by_name
from src.assembly_point__db.helpers.get_unit import get_unit_by_id


class AddLaunchResponse(BaseModel):
    data: Dict[str, Union[int, str]]
    stand: int


def api_add_launch(data: Dict[str, Any]) -> Dict[str, Any]:
    stand = data['stend']
    cmd = data['data']['cmd']
    algoritm = data['data']['algoritm']
    start = data['data']['start']
    end = data['data']['end']
    stage_count = data['data']['stage_count']
    places = data['data'].get('places', None)
    if places:
        algoritm_id = get_algoritm_id_by_name(name=algoritm).id
        unit_info_id = get_unit_by_id(stand).info
        add_launch(algoritm=algoritm_id,
                   unit_info=unit_info_id,
                   unit=stand,
                   start=start,
                   end=end,
                   stage_count=stage_count)
        launch_id = last_launch_id()
        report_id = next_report_id()
        for place in places:
            add_report(launch=launch_id, place=place.get('place'), mac=place.get('mac'), result=place.get('result'))
            add_log(report=report_id, stages=place.get('log'))
            add_measure(report=report_id, measure_list=place.get('measures'))
        data = {
            "cmd": cmd,
            "launch_id": last_launch_id()
        }
    else:
        algoritm_id = get_algoritm_id_by_name(name=algoritm).id
        unit_info_id = get_unit_by_id(stand).info
        add_launch(algoritm=algoritm_id,
                   unit_info=unit_info_id,
                   unit=stand,
                   start=start,
                   end=end,
                   stage_count=stage_count)
        data = {
            "cmd": cmd,
            "launch_id": last_launch_id()
        }
    result = AddLaunchResponse(data=data, stand=stand).dict()
    return result
