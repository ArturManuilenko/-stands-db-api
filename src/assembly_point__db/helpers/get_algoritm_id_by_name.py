from db_utils.utils.enshure_db_object_exists import enshure_db_object_exists

from src.assembly_point__db.model.calibration.algoritm_mysql import AlgoritmMySQL


def get_algoritm_id_by_name(name: str) -> AlgoritmMySQL:
    algoritm = AlgoritmMySQL.query.filter_by(name=name).first()
    return enshure_db_object_exists(AlgoritmMySQL, algoritm)
