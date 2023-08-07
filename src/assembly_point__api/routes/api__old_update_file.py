from typing import Dict, Any, Union

from pydantic import BaseModel

from src.assembly_point__db.helpers.get_update_file import get_update_file_by_path


class UpdateFileResponse(BaseModel):
    data: Dict[str, Union[int, str]]
    stand: int


def api_update_file(data: Dict[str, Any]) -> Dict[str, Any]:
    stend = data['stend']
    cmd = data['data']['cmd']
    path = data['data']['path']
    response = get_update_file_by_path(path)
    data = {
        "data": response.data.hex(),
        "cmd": cmd,
    }
    result = UpdateFileResponse(data=data, stand=stend).dict()
    return result
