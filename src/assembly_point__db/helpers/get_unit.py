from db_utils.utils.enshure_db_object_exists import enshure_db_object_exists

from src.assembly_point__db.model.calibration.unit_mysql import UnitMySQL


def get_unit_by_id(id: int) -> UnitMySQL:
    unit_id = UnitMySQL.query.filter_by(id=id).first()
    return enshure_db_object_exists(UnitMySQL, unit_id)
