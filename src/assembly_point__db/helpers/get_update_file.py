from db_utils.utils.enshure_db_object_exists import enshure_db_object_exists

from src.assembly_point__db.model.calibration.out_update_mysql import OutUpdateMySQL


def get_update_file_by_path(path: str) -> OutUpdateMySQL:
    update_file = OutUpdateMySQL.query.filter_by(path=path).first()
    return enshure_db_object_exists(OutUpdateMySQL, update_file)
