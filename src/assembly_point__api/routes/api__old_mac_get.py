from typing import Dict, Any, Union

from pydantic import BaseModel

from src.assembly_point__db.helpers.get_stend_list import get_stend_by_id
from src.assembly_point__db.helpers.table_name_model_map import TABLE_NAME_TO_MODEL__MAP


class MacGetResponse(BaseModel):
    data: Dict[str, Union[int, str]]
    stand: int


def api_mac_get(data: Dict[str, Any]) -> Dict[str, Any]:
    stend = data['stend']
    cmd = data['data']['cmd']
    # chip = data['data']['chip'] # ?????
    serial = data['data']['serial']
    stand = get_stend_by_id(stend).to_dict()
    table = stand['device_model']['mac_table']
    model = TABLE_NAME_TO_MODEL__MAP[table]
    result = model.query.filter_by(serial=serial).first()
    response = result.to_dict()
    data = {
        "mac": response['mac'],
        "cmd": cmd,
        "datetime": response['datetime']
    }
    result = MacGetResponse(data=data, stand=stend).dict()
    return result
