from src.assembly_point__db.model.work.pcb_type_mysql import PCBTypeMySQL


def get_pcb_type_by_id(pcb_id: int) -> PCBTypeMySQL:
    pcb_type = PCBTypeMySQL.query.filter_by(id=pcb_id).first()
    return pcb_type
