from db_utils.utils.enshure_db_object_exists import enshure_db_object_exists

from src.assembly_point__db.model.stend_control_schema.stend_update import StendUpdate


def get_stend_update_by_id(stend: int) -> StendUpdate:
    stend_update = StendUpdate.query.filter_by(stend=stend, enable=True)
    return enshure_db_object_exists(StendUpdate, stend_update)
