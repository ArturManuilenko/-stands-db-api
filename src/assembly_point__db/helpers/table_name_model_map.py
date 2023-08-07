from src.assembly_point__db.model.work.address_208s7_mysql import Address208s7MySQL
from src.assembly_point__db.model.work.address_208s7_ukr_mysql import Address208S7UkrMySQL
from src.assembly_point__db.model.work.address_318_mysql import Address318MySQL
from src.assembly_point__db.model.work.address_3ph_mysql import Address3PhMySQL
from src.assembly_point__db.model.work.address_fluo_mysql import AddressFluoMySQL
from src.assembly_point__db.model.work.address_k_mysql import AddressKMySQL
from src.assembly_point__db.model.work.address_l1_mysql import AddressL1MySQL
from src.assembly_point__db.model.work.address_l2_mysql import AddressL2MySQL
from src.assembly_point__db.model.work.address_l3_mysql import AddressL3MySQL
from src.assembly_point__db.model.work.address_lora_mysql import AddressloraMySQL
from src.assembly_point__db.model.work.address_modem_mysql import AddressModemMySQL
from src.assembly_point__db.model.work.address_mysql import AddressMySQL
from src.assembly_point__db.model.work.address_opto_mysql import AddressOptoMySQL
from src.assembly_point__db.model.work.lora_keys_mysql import LoraKeysMySQL
from src.assembly_point__db.model.work.vaviot_keys_mysql import VaviotKeysMySQL

TABLE_NAME_TO_MODEL__MAP = {
    'address_3ph': Address3PhMySQL,
    'address_208s7': Address208s7MySQL,
    'address_208s7_ukr': Address208S7UkrMySQL,
    'address_318': Address318MySQL,
    'address_fluo': AddressFluoMySQL,
    'address_k': AddressKMySQL,
    'address_l1': AddressL1MySQL,
    'address_l2': AddressL2MySQL,
    'address_l3': AddressL3MySQL,
    'address_lora': AddressloraMySQL,
    'address_modem': AddressModemMySQL,
    'address': AddressMySQL,
    'address_opto': AddressOptoMySQL,
    'vaviot_keys': VaviotKeysMySQL,
    'lora_keys': LoraKeysMySQL,
}
