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
launch_id = form.getvalue('launch')

html = html_nero.HtmlBase("Данные поверки/калибровки прибора", 'calibration.calibrinfo', 'Данные')

connection = db.connect(**DB_CONFIG, database='calibration')
cursor = connection.cursor(dictionary=True, buffered=True)

if report_id:
    cursor.execute("SELECT id,place,mac FROM report WHERE id=%s;", (report_id,))
elif launch_id:
    cursor.execute("SELECT id,place,mac FROM report WHERE launch=%s ORDER BY place;", (launch_id,))

tbl = html_blocks.Table(cssclass='')
tbl.set_header(
    'Фаза', 'Группа', 'Тип', 'Значение', 'Погрешность'
)
for rep in cursor:
    editlink = ''
    if html.access_info['edit_protocol']:
        editlink = ' <a href="calibredit.py?id={}"><img src="/icons/edit.png" height=16></a>'.format(rep['id'])
    tbl.add_row(('<b>Прибор <a href="calibrdevlist.py?mac={mac}">{mac}</a> на месте {place} отчет ' \
                '<a href="calibrlog.py?id={id}">{id}</a>{editlink}</b>'.format(
        mac=rep['mac'], place=rep['place'] + 1, id=rep['id'], editlink=editlink), 'colspan="5"'))

    cursor1 = connection.cursor(dictionary=True, buffered=True)
    cursor1.execute("SELECT `id`,`group`,`type`,`phase`,`error`,`value`,`result` "
                    "FROM `measure` "
                    "WHERE `report`=%s ORDER BY `id`;", (rep['id'],))
    for row in cursor1:
        result = 'ok' if row['result'] else 'fail'
        tbl.add_row(
            row['phase'],
            row['group'],
            row['type'],
            ('{}'.format(row['value']) if row['value'] is not None else '', 'class="result-{}"'.format(result)),
            ('{:f}%'.format(row['error']) if row['error'] is not None else '', 'class="result-{}"'.format(result)),
        )

html.add(tbl)
html.print()
