from db_utils.utils.enshure_db_object_exists import enshure_db_object_exists

from src.assembly_point__db.model.calibration.report_mysql import ReportMySQL


def get_last_report_by_mac(mac: int) -> ReportMySQL:
    report = ReportMySQL.query.filter_by(mac=mac).order_by(ReportMySQL.id.desc()).first()
    return enshure_db_object_exists(ReportMySQL, report)
