#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import mysql.connector as db

import cgitb

from src.assembly_point__old_web.env import DB_CONFIG

cgitb.enable()

connection = None

def connect():
    global connection
    if not connection:
        connection = db.connect(**DB_CONFIG, database='web')
    return connection

def access(token):
    login = None
    token_data = token.split('-')
    if len(token_data) == 3:
        login = token_data[0]
        cn = connect()
        cursor = cn.cursor(dictionary=True)
        cursor.execute(''' SELECT id,token,admin,protocol,edit_protocol FROM web_access WHERE login=%s;''',(login,))
        for res in cursor.fetchall():
            if token == res['token']:
                return {
                        'id': res['id'],
                        'login': login,
                        'admin': res['admin'], # администратор - подтверждение контрольных сумм и блокировок
                        'protocol': res['protocol'], # добавление протокола
                        'edit_protocol': res['edit_protocol'], # редактирование протокола
                        }
    return {'login': None, 'admin': False, 'protocol': False, 'edit_protocol': False}

def config(login, param):
    value = ''
    cn = connect()
    cursor = cn.cursor(dictionary=False)
    cursor.execute(''' SELECT value FROM web_access, web_user_config WHERE web_access.id=web_user_config.user_id AND login=%s AND param=%s;''',(login,param))
    res = cursor.fetchone()
    if res:
        value = res[0]
    return value

def get_web_user_info(login_email):
    cn = connect()
    cursor = cn.cursor(dictionary=False)
    cursor.execute('''SELECT login,passhash FROM web_access WHERE login=%s OR email=%s;''', (login_email, login_email))
    res = cursor.fetchone()
    if res:
        return res[0], res[1]
    else:
        return None

def set_token(login, token):
    cn = connect()
    cursor = cn.cursor(dictionary=False)
    cursor.execute('''UPDATE web_access SET token=%s WHERE login=%s;''', (token, login))
    cn.commit()


def set_stend_crc(stend, param, platform):
    cn = connect()
    cursor = cn.cursor(dictionary=False)
    cursor.execute('''REPLACE INTO stend_control_schema.stend_crc (id,time,param,platform) VALUES(%s,now(),%s,%s);''', (stend, param, platform))
    cn.commit()


def set_stend_config(stend, type, value):
    cn = connect()
    cursor = cn.cursor(dictionary=False)
    config = None
    cursor.execute("SELECT id FROM stend_control_schema.stend_config_ids WHERE name=%s",(type,))
    for row in cursor:
        config = row[0]

    if config is not None:
        cursor.execute("UPDATE `stend_control_schema`.`stend_config` SET `value`=%s, `timestamp`=now() "
                       "WHERE `stend`=%s AND `config`=%s;",
                       (value, stend, config))
        if cursor.rowcount == 0:
            cursor.execute("INSERT INTO `stend_control_schema`.`stend_config` (`stend`,`config`,`value`) "
                           "VALUES(%s,%s,%s);",
                           (stend, config, value))
    cn.commit()


def set_stend_update_enable(stend, file, en):
    cn = connect()
    cursor = cn.cursor(dictionary=False)
    cursor.execute("UPDATE `stend_control_schema`.`stend_update` SET `enable`=%s "
                    "WHERE `stend`=%s AND `name`=%s;",
                    (en, stend, file))
    cn.commit()


def register_stend_config(stend, file):
    cn = connect()
    cursor = cn.cursor(dictionary=False)
    if file == 'param':
        cursor.execute("INSERT INTO `stend_control_schema`.`stend_crc` (id, time, param, platform) "
                       "VALUES(%s, now(), (SELECT `crc32` FROM `stend_control_schema`.`current_config_files` WHERE `stend`=%s AND `name`='param'), 0) "
                       "ON DUPLICATE KEY UPDATE time=now(), param=(SELECT `crc32` FROM `stend_control_schema`.`current_config_files` WHERE `stend`=%s AND `name`='param')",
                        (stend,stend,stend))

        cursor.execute("INSERT IGNORE INTO `stend_control_schema`.`firm_files` (`type`,`time`,`repository`,`comment`,`name`,`md5`,`crc32`,`data`,`version`) "
                       "SELECT 'O',now(),'','',`name`,`md5`,`crc32`,`data`,`version` FROM `stend_control_schema`.`current_config_files` WHERE `stend`=%s AND `name`='param';",
                       (stend, )
                       )

        cursor.execute("SELECT `id` FROM `stend_control_schema`.`firm_files` WHERE `md5` IN "
                       "(SELECT `md5` FROM `stend_control_schema`.`current_config_files` WHERE `stend`=%s AND `name`='param')",
                       (stend,)
                       )
        for file_id in cursor.fetchall():
            cursor.execute("INSERT `stend_control_schema`.`stend_update` (`stend`,`name`,`file`,`enable`) VALUES (%s,'param',%s,0) "
                           "ON DUPLICATE KEY UPDATE `file`=%s",
                           (stend,file_id[0],file_id[0])
                           )

    if file == 'platform':
        cursor.execute("INSERT INTO `stend_control_schema`.`stend_crc` (id, time, param, platform) "
                       "VALUES(%s, now(), 0, (SELECT `crc32` FROM `stend_control_schema`.`current_config_files` WHERE `stend`=%s AND `name`='platform')) "
                       "ON DUPLICATE KEY UPDATE `time`=now(), `platform`=(SELECT `crc32` FROM `stend_control_schema`.`current_config_files` WHERE `stend`=%s AND `name`='platform')",
                        (stend,stend,stend))

        cursor.execute("INSERT IGNORE INTO `stend_control_schema`.`firm_files` (`type`,`time`,`repository`,`comment`,`name`,`md5`,`crc32`,`data`,`version`) "
                       "SELECT 'O',now(),'','',`name`,`md5`,`crc32`,`data`,`version` FROM `stend_control_schema`.`current_config_files` WHERE `stend`=%s AND `name`='platform';",
                       (stend, )
                       )

        cursor.execute("SELECT `id` FROM `stend_control_schema`.`firm_files` WHERE `md5` IN "
                       "(SELECT `md5` FROM `stend_control_schema`.`current_config_files` WHERE `stend`=%s AND `name`='platform')",
                       (stend,)
                       )
        for file_id in cursor.fetchall():
            cursor.execute("INSERT `stend_control_schema`.`stend_update` (`stend`,`name`,`file`,`enable`) VALUES (%s,'platform',%s,0) "
                           "ON DUPLICATE KEY UPDATE `file`=%s",
                           (stend,file_id[0],file_id[0])
                           )
    cn.commit()


def edit_modification(id, name = None, model = None, descr = None):
    cn = connect()
    cursor = cn.cursor(dictionary=False)
    if name:
        cursor.execute('''UPDATE stend_control_schema.modification_list SET name=%s WHERE id=%s;''', (name, id))
    if model is not None:
        cursor.execute('''UPDATE stend_control_schema.modification_list SET model=%s WHERE id=%s;''', (model, id))
    if descr is not None:
        cursor.execute('''UPDATE stend_control_schema.modification_list SET description=%s WHERE id=%s;''', (descr, id))
    if cursor.rowcount == 0 and name and len(name):
        cursor.execute('''INSERT INTO stend_control_schema.modification_list (name,model,description) VALUES(%s,%s,%s);''', (
            name, model if model else '', descr if descr else name
            ))
    cn.commit()


def del_modification(id):
    cn = connect()
    cursor = cn.cursor(dictionary=False)
    cursor.execute('''DELETE FROM stend_control_schema.modification_list WHERE id=%s;''', (id,))
    cn.commit()


def protocol_device_info(mac):
    cn = connect()
    cursor = cn.cursor(dictionary=False)
    cursor.execute('SELECT `report`.`id`, `launch`.`end`,`alg`.`name` FROM `calibration`.`report` AS `report` '\
                    'JOIN `calibration`.`launch` AS `launch` ON `report`.`launch`=`launch`.`id` '\
                    'JOIN `calibration`.`algoritm` AS `alg` ON `launch`.`algoritm`=`alg`.`id` '\
                    'WHERE `mac`=%s AND result="000-ok" AND `launch`.`algoritm`!=0 '\
                    'ORDER BY `report`.`id` DESC LIMIT 1;', (mac, ))
    for row in cursor:
        return {'mac':mac, 'id':row[0], 'datetime':row[1].strftime('%Y-%m-%d %H:%M:%S'), 'algoritm':row[2]}


def add_protocol(launch, number, fio, t, f, p, lab, places, reports):
    cn = connect()
    cursor = cn.cursor(dictionary=False)
    cursor.execute('INSERT INTO `calibration`.`protocol` (`number`,`fio`,`t`,`f`,`p`,`lab`) '\
    'VALUES (%s,%s,%s,%s,%s,%s);', (number, fio, t, f, p, lab))
    proto_id = cursor.lastrowid

    for pl in places:
        cursor.execute('INSERT INTO `calibration`.`protocol_reports` (`report`,`protocol`) VALUES '\
            '((SELECT id FROM `calibration`.`report` WHERE launch=%s AND place=%s),%s);',
                   (launch, pl, proto_id))

    for rep in reports:
        cursor.execute('INSERT INTO `calibration`.`protocol_reports` (`report`,`protocol`) VALUES (%s,%s);',
                   (rep, proto_id))

    cn.commit()


def add_version(id, version, variant, hard):
    cn = connect()
    cursor = cn.cursor(dictionary=False)
    cursor.execute('INSERT INTO `smarthome`.`versions` (`id`,`version`,`variant`,`hard`,`allow`) VALUES (%s,%s,%s,%s,1);',
                   (id, version, variant, hard))
    cn.commit()


def lock_version(number):
    cn = connect()
    cursor = cn.cursor(dictionary=False)
    cursor.execute('UPDATE `smarthome`.`versions` SET allow=0, close_time=now() WHERE `number`=%s;',
                   (number, ))
    cn.commit()


def add_stend_group(name):
    cn = connect()
    cursor = cn.cursor(dictionary=False)
    cursor.execute('INSERT INTO `stend_control_schema`.`stend_groups` (`name`) VALUES(%s);',
                   (name, ))
    cn.commit()


def del_stend_group(id):
    cn = connect()
    cursor = cn.cursor(dictionary=False)
    cursor.execute('DELETE FROM `stend_control_schema`.`stend_groups` WHERE `id`=%s;',
                   (id, ))
    cn.commit()


def modify_stend_group(id, name, add_stend, del_stend):
    cn = connect()
    cursor = cn.cursor(dictionary=False)
    if name is not None:
        cursor.execute('UPDATE `stend_control_schema`.`stend_groups` SET `name`=%s;',
                   (name, ))
    if del_stend is not None:
        cursor.execute('DELETE FROM `stend_control_schema`.`stend_group_bind` WHERE `group`=%s AND `stend`=%s;',
                   (id, del_stend))
    if add_stend is not None:
        cursor.execute('INSERT INTO `stend_control_schema`.`stend_group_bind` (`group`,`stend`) VALUES(%s,%s);',
                   (id, add_stend))
    cn.commit()


def modify_calibr_result(id, result):
    cn = connect()
    cursor = cn.cursor(dictionary=False)

    cursor.execute('UPDATE `calibration`.`report` SET result=%s WHERE `id`=%s;',
                (result, id))

    cn.commit()


def modify_calibr_measure(id, error, value, etalon, result):
    cn = connect()
    cursor = cn.cursor(dictionary=False)

    cursor.execute('UPDATE `calibration`.`measure` SET `error`=%s, `value`=%s, `etalon`=%s, result=%s WHERE `id`=%s;',
                (error, value, etalon, result, id))

    cn.commit()
