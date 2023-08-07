#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cgi
import cgitb
import html_nero
import html_blocks

import mysql.connector as db

from src.assembly_point__old_web.env import DB_CONFIG

cgitb.enable()

form = cgi.FieldStorage()
launch = int(form.getvalue('launch', 0))

html = html_nero.HtmlBase("Добавление протокола поверки", 'calibration.addprotocol', 'Добавление протокола поверки')
html.add_js_files('/js/value_editor.js')
html.add_css_files('/css/value_editor.css')

html.add_js_files('/js/addprotocol.js')

if html.access_info['protocol']:
    connection = db.connect(**DB_CONFIG, database='calibration')
    cursor = connection.cursor(dictionary=True)

    # редактирование
    cmd = '''{{cmd: 'calibr_add_protocol', launch:{}}}'''.format(launch)

    form = html_blocks.EditForm(group_apply=True, command=cmd)

    devs = []
    if launch != 0:
        cursor.execute("SELECT `report`.id,place,mac,protocol FROM `report` "
                       "LEFT JOIN `protocol_reports` ON `report`.`id`=`report` WHERE `launch`=%s AND `result`='000-ok';",
                       (launch,))
        for row in cursor:
            if row['protocol'] is None:
                devs.append((row['place'], row['mac']))

    if len(devs) == 0 and launch != 0:
        form.add_row('').add_text('Нет устройств для добавления в протокол')
    else:
        labs = []
        cursor.execute("SELECT id,name FROM `laboratory`;")
        for row in cursor:
            labs.append((row['id'], row['name']))

        fio = ''
        cursor.execute("SELECT fio FROM web.user_info WHERE id=%s;", (html.access_info['id'],))
        for row in cursor:
            fio = row['fio']

        form.add_row('№ протокола').add_text_edit('number', '')
        form.add_row('ФИО поверителя').add_text_edit('fio', fio)
        form.add_row('Лаборатория').add_combo_box('lab', labs)
        form.add_row('Температура,°С').add_text_edit('t', '0')
        form.add_row('Давление,кПА').add_text_edit('p', '0')
        form.add_row('Относительная влажность,%').add_text_edit('f', '0')

        if launch == 0:
            form.add_row('Добавить адрес').add_text_edit('', '').add_button('добавить', None, 'add_mac(this);')

        for place, mac in devs:
            form.add_row('Место {}'.format(place + 1)).add_check_box('pl{}'.format(place),
                                                                  ' адрес {}'.format(mac), checked=True)

        form.add_group_buttons(cmd, btn_apply='Создать')

    html.add(form)

html.print()
