from db_utils.utils.enshure_db_object_exists import enshure_db_object_exists

from src.assembly_point__db.model.stend_control_schema.firm_files import FirmFiles


def get_firm_files_by_id(file_id: int) -> FirmFiles:
    firm_data = FirmFiles.query.filter_by(id=file_id).first()
    return enshure_db_object_exists(FirmFiles, firm_data)
