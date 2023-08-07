from typing import Dict, Callable
from flask import request
from api_utils.utils.constants import TJsonResponse

from src.assembly_point__api.flask import flask_app
from src.assembly_point__api.routes.api__old_add_launch import api_add_launch
from src.assembly_point__api.routes.api__old_add_log import api_add_log
from src.assembly_point__api.routes.api__old_add_measure import api_add_measure
from src.assembly_point__api.routes.api__old_calibration_add_report import api_calibration_add_report
from src.assembly_point__api.routes.api__old_get_key import api_get_key
from src.assembly_point__api.routes.api__old_firm_data import api_firm_data
from src.assembly_point__api.routes.api__old_firm_info import api_firm_info
from src.assembly_point__api.routes.api__old_firm_upd_rep import api_firm_upd_rep
from src.assembly_point__api.routes.api__old_info import api_info
from src.assembly_point__api.routes.api__old_last_report import api_last_report
from src.assembly_point__api.routes.api__old_mac_alloc import api_mac_alloc
from src.assembly_point__api.routes.api__old_mac_get import api_mac_get
from src.assembly_point__api.routes.api__old_pcb_data import api_pcb_type
from src.assembly_point__api.routes.api__old_report_add import api_report_add
from src.assembly_point__api.routes.api__old_update_file import api_update_file
from src.assembly_point__api.routes.api__old_update_list import api_update_list

CMD_API__MAP: Dict[str, Callable] = {
    'info': api_info,
    'mac_get': api_mac_get,
    'mac_alloc': api_mac_alloc,
    'pcb_data': api_pcb_type,
    'get_key': api_get_key,
    'firm_data': api_firm_data,
    'firm_info': api_firm_info,
    'firm_upd_rep': api_firm_upd_rep,
    'report_add': api_report_add,
    'add_measure': api_add_measure,
    'update_file': api_update_file,
    'update_list': api_update_list,
    'last_report': api_last_report,
    'add_log': api_add_log,
    'add_report': api_calibration_add_report,
    'add_launch': api_add_launch
}


@flask_app.route('/',)
def ap_old_api() -> TJsonResponse:
    data = request.get_json()
    cmd = data['data']['cmd']
    command = CMD_API__MAP.get(cmd, None)
    if command is not None:
        return command(data)
    return 'BadResponse, 400'
