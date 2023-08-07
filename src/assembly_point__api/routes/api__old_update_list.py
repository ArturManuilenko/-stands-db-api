from typing import Dict, Any, Union, List
from pydantic import BaseModel

from src.assembly_point__db.helpers.get_update_list import get_update_list


class UpdateListResponse(BaseModel):
    data: Dict[str, Union[List, str]]
    stand: int


def api_update_list(data: Dict[str, Any]) -> Dict[str, Any]:
    stend = data['stend']
    cmd = data['data']['cmd']
    update_list = get_update_list()
    data = {"files": [{
        "path": update.path,
        "md5": update.md5} for update in update_list],
        "cmd": cmd
    }
    result = UpdateListResponse(data=data, stand=stend).dict()
    return result
