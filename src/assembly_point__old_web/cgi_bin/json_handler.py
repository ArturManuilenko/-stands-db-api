#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import json
import db
import traceback

import http.cookies
import cgi
import cgitb

from exec.client_tcp import TCPClient

cgitb.enable()

cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
user_token = cookie.get("user_token")

result = {}

form = cgi.FieldStorage(keep_blank_values=1)
cmd = form.getvalue('cmd')


class HandlerException(Exception):
    def __init__(self, text: str) -> None:
        self.text = text

    def __str__(self) -> str:
        return self.text


def check_rights(*rights):
    errs = {'admin': 'Необходимы права на администрирование',
            'protocol': 'Необходимы права на регистрацию протокола',
            }

    if user_token:
        access_rights = db.access(user_token.value)
        for r in rights:
            if type(r) is str:
                if not access_rights.get(r, False):
                    print('Content-Type: application/json\n\n')
                    print(json.dumps({'error': errs.get(r, 'Не достаточно прав')}))
                    exit()
            else:
                if not True in [access_rights.get(rm, False) for rm in r]:
                    raise HandlerException(
                        ' или \n'.join(errs.get(rm, 'Не достаточно прав') for rm in r)
                        )

        return access_rights
    else:
        print('Content-Type: application/json\n\n')
        print(json.dumps({'error': 'Необходимо выполнить авторизацию'}))
        exit()

try:
    if cmd == 'progress':
        form_id = form.getvalue('id')
        cl = TCPClient(form_id)
        progress, ready = cl.check_progress()
        result['value'] = progress
        result['ready'] = ready
    elif cmd == 'result_html':
        form_id = form.getvalue('id')
        cl = TCPClient(form_id)
    elif cmd == 'keep':
        form_id = form.getvalue('id')
        cl = TCPClient(form_id)
        cl.keep()
    elif cmd == 'resultfile':
        form_id = form.getvalue('id')
        cl = TCPClient(form_id)
        data, files = cl.get_data()
        result = {'filename': str(files[0])}

    elif cmd == 'modify_stend':
        form_id = form.getvalue('id')
        descr = form.getvalue('descr')
        crc_param = form.getvalue('crc_param')
        crc_platform = form.getvalue('crc_platform')
        if descr:
            check_rights('admin')
            result = {'error': 'descr'}
        if crc_param and crc_platform:
            check_rights('admin')
            db.set_stend_crc(form_id, int(crc_param, 16), int(crc_platform, 16))

    elif cmd == 'modify_stend_config':
        form_id = form.getvalue('id')
        check_rights('admin')
        for cfg in form.keys():
            if cfg not in ['id', 'cmd']:
                db.set_stend_config(form_id, cfg, form.getvalue(cfg))

    elif cmd == 'modify_stend_update_en':
        form_id = form.getvalue('id')
        check_rights('admin')
        file = form.getvalue('file')
        en = form.getvalue('enabled', 0)
        if file is None:
            raise HandlerException('Не указан файл')
        db.set_stend_update_enable(form_id, file, int(en))

    elif cmd == 'register_stend_config':
        form_id = form.getvalue('id')
        check_rights('admin')
        file = form.getvalue('file')
        if file is None:
            raise HandlerException('Не указан файл')
        db.register_stend_config(form_id, file)

    elif cmd == 'modify_mod':
        form_id = form.getvalue('id')
        name = form.getvalue('name')
        model = form.getvalue('model')
        descr = form.getvalue('descr')
        check_rights('admin')
        db.edit_modification(form_id, name, model, descr)

    elif cmd == 'del_mod':
        form_id = form.getvalue('id')
        check_rights('admin')
        db.del_modification(form_id)

    elif cmd == 'protocol_device_info':
        mac = int(form.getvalue('mac'))
        res = db.protocol_device_info(mac)
        if res is None:
            raise HandlerException('Отчет не найден')
        result = {'mac': res['mac'], 'report': res['id'], 'datetime': res['datetime'], 'algoritm': res['algoritm']}

    elif cmd == 'calibr_add_protocol':
        launch = int(form.getvalue('launch'))
        number = form.getvalue('number')
        fio = form.getvalue('fio')
        t = float(form.getvalue('t'))
        f = float(form.getvalue('f'))
        p = float(form.getvalue('p'))
        lab = float(form.getvalue('lab'))
        places = []

        for n in range(48):
            pl = form.getvalue('pl{}'.format(n))
            if pl and pl == '1':
                places.append(n)

        reports = []
        n = 0
        while True:
            rep = form.getvalue('report{}'.format(n), None)
            if rep is None:
                break
            n += 1
            reports.append(rep)

        check_rights('protocol')

        if len(places) == 0 and len(reports) == 0:
            raise HandlerException('Нет устройств для добавления в протокол')

        db.add_protocol(launch, number, fio, t, f, p, lab, places, reports)

    elif cmd == 'lock_version':
        check_rights('admin')
        number = int(form.getvalue('number'))
        db.lock_version(number)

    elif cmd == 'add_version':
        check_rights('admin')
        version = form.getvalue('version').split('.')
        if len(version) != 4: raise HandlerException('Неверный формат версии')
        for v in version:
            if not 0 < int(v) < 256: raise HandlerException('Неверный формат версии')

        db.add_version(version[0],version[1],version[2],version[3])

    elif cmd == 'add_stend_group':
        check_rights('admin')
        name = form.getvalue('name')
        if name == '':
            raise HandlerException('Название не может быть пустой строкой')
        db.add_stend_group(name)

    elif cmd == 'del_stend_group':
        check_rights('admin')
        form_id = int(form.getvalue('id'))
        db.del_stend_group(form_id)

    elif cmd == 'modify_stend_group':
        check_rights('admin')
        form_id = int(form.getvalue('id'))
        db.modify_stend_group(form_id,
                              name=form.getvalue('name'),
                              add_stend=form.getvalue('add'),
                              del_stend=form.getvalue('del'))

    elif cmd == 'modify_calibr_result':
        check_rights('edit_protocol')

        form_id = int(form.getvalue('id'))
        result = form.getvalue('result')

        db.modify_calibr_result(form_id, result)

    elif cmd == 'modify_calibr_measure':
        check_rights('edit_protocol')

        form_id = int(form.getvalue('id'))
        error = form.getvalue('error')
        error = None if error == '' else float(error)
        value = form.getvalue('value')
        value = None if value == '' else float(value)
        etalon = form.getvalue('etalon')
        etalon = None if etalon == '' else float(etalon)

        result = int(form.getvalue('result'))

        db.modify_calibr_measure(form_id, error, value, etalon, result)
    else:
        raise HandlerException('Неизвестная команда {}'.format(cmd))

except HandlerException as e:
    result = {'error': str(e)}
except Exception as e:
    tb1 = traceback.TracebackException.from_exception(e)
    result = {'error': ''.join(tb1.format()) + str(e)}

print('Content-Type: application/json\n\n')
print(json.dumps(result))
