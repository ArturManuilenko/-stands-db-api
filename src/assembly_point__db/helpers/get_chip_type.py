from db_utils.utils.enshure_db_object_exists import enshure_db_object_exists

from src.assembly_point__db.model.work.chip_type_mysql import ChipTypeMySQL


def get_chip_by_id(descr: str) -> ChipTypeMySQL:
    chip = ChipTypeMySQL.query.filter_by(descr=descr).first()
    return enshure_db_object_exists(ChipTypeMySQL, chip)