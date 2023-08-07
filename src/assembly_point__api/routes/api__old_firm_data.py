from typing import Dict, Any, Union
from pydantic import BaseModel

from src.assembly_point__db.helpers.get_firm_files import get_firm_files_by_id


class FirmDataResponse(BaseModel):
    data: Dict[str, Union[int, str, bytes, None]]
    stand: int


def api_firm_data(data: Dict[str, Any]) -> Dict[str, Any]:
    stend = data['stend']
    cmd = data['data']['cmd']
    file_id = data['data']['file_id']
    firm_data = get_firm_files_by_id(file_id)
    data = {
        "data": firm_data.data.hex(),
        "version": firm_data.version,
        "md5": firm_data.md5,
        "type": firm_data.type,
        "cmd": cmd,
        "comment": firm_data.comment,
        "file_id": file_id,
        "repository": firm_data.repository,
    }
    result = FirmDataResponse(data=data, stand=stend).dict()
    return result
