from db_utils.utils.enshure_db_object_exists import enshure_db_object_exists

from src.assembly_point__db.model.stend_control_schema.stend_list import StendList


def get_stend_by_id(stend_id: int) -> StendList:
    stend = StendList.query.filter_by(stend_id=stend_id).first()
    return enshure_db_object_exists(StendList, stend)
