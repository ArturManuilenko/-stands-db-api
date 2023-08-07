from datetime import datetime
from typing import Dict, Any, Tuple, Optional
from db_utils.modules.db import db
from sqlalchemy import func
from sqlalchemy.sql.operators import exists

from src.assembly_point__db.helpers.table_name_model_map import TABLE_NAME_TO_MODEL__MAP


def add_mac_standard(data: Dict[str, Any], model, serial, chip_id) -> Tuple[Optional[int], str, datetime]:
    max_mac = db.session.query(func.max(model.mac)).scalar()
    mac_max = data['device_model']['mac_end']
    mac_min = data['device_model']['mac_start']
    if max_mac is None or max_mac < mac_min:
        mac = mac_min
    else:
        mac = max_mac + 1
    if mac <= mac_max:
        if serial is None:
            serial = '{:08X}{}'.format(mac, '0' * 24)
        mac_datetime = datetime.now()
        db.session.add(model(mac=mac, datetime=mac_datetime, serial=serial, chip_id=chip_id))
        db.session.commit()
    else:
        mac, mac_datetime = None, None
    return mac, serial, mac_datetime


def add_mac_pool(data: Dict[str, Any], model, serial, chip_id) -> Tuple[Optional[int], str, datetime]:
    pool_model = TABLE_NAME_TO_MODEL__MAP[data['device_model']['pool_table']]
    pool_group = data['device_model']['mac_start']
    mac = db.session.query(func.min(pool_model.mac)).filter(pool_model.group == pool_group).filter(~exists().where(model.mac == pool_model.mac))
    if serial is None:
        serial = '{:08X}{}'.format(mac, '0' * 24)
    mac_datetime = datetime.now()
    db.session.add(model(mac=mac, datetime=mac_datetime, serial=serial, chip_id=chip_id))
    db.session.commit()
    return mac, serial, mac_datetime


def add_mac(data: Dict[str, Any], model, serial, chip_id) -> Tuple[Optional[int], str, datetime]:
    if data['device_model']['pool_table'] is None:
        return add_mac_standard(data, model, serial, chip_id)
    return add_mac_pool(data, model, serial, chip_id)
