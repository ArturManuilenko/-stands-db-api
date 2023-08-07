from typing import Dict, Any, Union
from pydantic import BaseModel

from src.assembly_point__db.helpers.add_mac import add_mac
from src.assembly_point__db.helpers.get_chip_type import get_chip_by_id
from src.assembly_point__db.helpers.get_stend_list import get_stend_by_id
from src.assembly_point__db.helpers.table_name_model_map import TABLE_NAME_TO_MODEL__MAP


class MacAllocResponse(BaseModel):
    data: Dict[str, Union[int, str]]
    stand: int


def api_mac_alloc(data: Dict[str, Any]) -> Dict[str, Any]:
    stend = data['stend']
    cmd = data['data']['cmd']
    chip = data['data'].get('chip', 'freescale')
    chip_id = get_chip_by_id(chip).id
    serial = data['data'].get('serial', None)
    stand = get_stend_by_id(stend).to_dict()
    table = stand['device_model']['mac_table']
    model = TABLE_NAME_TO_MODEL__MAP[table]
    result = model.query.filter_by(serial=serial).first()
    if result:
        response = result.to_dict()
        data = {
            "new": 0,
            "mac": response['mac'],
            "serial": response['serial'],
            "cmd": cmd,
            "datetime": response['datetime']
        }
    else:
        if stand['generate'] == 0:
            return 'BadResponse, 400'
        mac, serial, mac_datetime = add_mac(stand, model, serial, chip_id)
        data = {
            "new": 1,
            "serial": serial,
            "mac": mac,
            "cmd": cmd,
            "datetime": mac_datetime.isoformat()
        }
    result = MacAllocResponse(data=data, stand=stend).dict()
    return result
