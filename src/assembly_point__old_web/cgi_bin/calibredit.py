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
report_id = form.getvalue('id')

html = html_nero.HtmlBase("Редактирование показаний поверки/калибровки прибора", 'calibration.calibredit', 'Редактирование показаний')
html.add_js_files('/js/value_editor.js')
html.add_css_files('/css/value_editor.css')

if not html.access_info['edit_protocol']:
    html.add('Доступ запрещен')
else:
    connection = db.connect(**DB_CONFIG, database='calibration')
    cursor = connection.cursor(dictionary=False, buffered=True)

    cursor.execute("SELECT COUNT(*) FROM `protocol_reports` WHERE `report`=%s;", (report_id,))
    row = cursor.fetchall()[0]
    if row[0] > 0:
        html.add('Запрещено редактировать результаты поверки прибора, добавленного в протокол')
    else:
        cursor.execute("SELECT COUNT(*) FROM `measure` WHERE `report`=%s AND `result`=0;", (report_id,))
        measure_fails = cursor.fetchall()[0][0]

        cursor.execute("SELECT `id`,`place`,`mac`,`result` FROM `report` WHERE `id`=%s;", (report_id,))
        row = cursor.fetchall()[0]

        form = html_blocks.EditForm()
        form.add_info('ID', '{}'.format(row[0]))
        form.add_info('Место', '{}'.format(row[1]))
        form.add_info('MAC', '{}'.format(row[2]))
        cell_make_ok = form.add_row('Результат').add_text('{}'.format(row[3]))
        if row[3] != '000-ok' and measure_fails == 0:
            cell_make_ok.add_button('Перевести в успешные', '''{{cmd: 'modify_calibr_result', id: {}, result:'000-ok'}}'''.format(report_id))
        form.add_info('Измерения:', '')

        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT `id`,`group`,`type`,`phase`,`error`,`value`,`etalon`,`result` "
            "FROM `measure` "
            "WHERE `report`=%s ORDER BY `id`;", (report_id,))

        for row in cursor:
            def val_text(value):
                return '{}'.format(value) if value is not None else ''

            cmd = '''{{cmd: 'modify_calibr_measure', id: {}}}'''.format(row['id'])
            form.add_row('<span style="background-color:{};">{} {} {}</span>'.format(
                '#B0FFB0' if row['result'] else '#FFB0B0', row['phase'], row['group'], row['type']), None, cmd)\
                .add_text('Погрешность:').add_text_edit('error', val_text(row['error']))\
                .add_text('Значение:').add_text_edit('value', val_text(row['value']))\
                .add_text('Эталон:').add_text_edit('etalon', val_text(row['etalon']))\
                .add_check_box('result', 'норма', '', row['result'])

        html.add(form)

html.print()
