#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cgi
import cgitb
import html_nero
import html_blocks

import mysql.connector as db
import math

from src.assembly_point__old_web.env import DB_CONFIG

cgitb.enable()

form = cgi.FieldStorage()
sort = form.getvalue('sort', 'id-')
page = form.getvalue('page', '1')
try:
    page = int(page)
except:
    page = 1

#sql sort-user sort-group sort-status
orders = {
    'id': 'p.id',
    'id-': 'p.id DESC',
    'number': 'number',
    'number-': 'number DESC',
    'time': 'time',
    'time-': 'time DESC',
}
order = orders.get(sort, orders['id-'])

html = html_nero.HtmlBase("Протоколы поверки", 'report.calibrprotocol')

if html.access_info['admin']:
    html.add_js_files('/js/commands.js')

connection = db.connect(**DB_CONFIG, database='calibration')
cursor = connection.cursor(dictionary=False)
cursor.execute("SELECT COUNT(*) FROM `protocol`;")
record_count = cursor.fetchall()[0][0]
page_size = 20
page_count = math.ceil(record_count / page_size)


cursor = connection.cursor(dictionary=True, buffered=True)
cursor.execute("SELECT p.`id`,p.`number`,p.`fio`,p.`t`,p.`f`,p.`p`,p.`time`,l.`name`,l.`descr` FROM `protocol` p "
               "JOIN `laboratory` l ON p.`lab` = l.`id`"
               "ORDER BY {} LIMIT {} OFFSET {};".format(order, page_size, (page - 1) * page_size))

def sortlink(caption, key):
    fmt = '<a href="calibrprotocol.py?sort={}&page={}">{}{}</a>'
    if sort == key:
        return fmt.format(key + '-', page, '<img src="/icons/sort-up.png" height=16>', caption)
    elif sort == key + '-':
        return fmt.format(key, page, '<img src="/icons/sort-down.png" height=16>', caption)
    else:
        return fmt.format(key, page, '', caption)

tbl = html_blocks.Table()
tbl.caption = 'Протоколы поверки'
tbl.set_header(
              (sortlink('ID', 'id'), 'class="cell-min-width"'),
              (sortlink('Номер', 'number'), 'class="cell-min-width"'),
              ('Дата', 'class="cell-min-width"'),
              (sortlink('Время регистрации', 'time'), 'class="cell-min-width"'),
              ('Приборов', 'class="cell-min-width"'),
              'Лаборатория',
              'Поверитель',
              'Установка',
              'Условия',
              ('','class="cell-buttons"'),
              )

for row in cursor:
    cursor1 = connection.cursor(dictionary=True)
    cursor1.execute("SELECT l.`id`,u.`name`,ui.`descr`,l.`end` FROM `launch` l "
                "JOIN `unit` u ON u.id=l.unit "
                "JOIN `unit_info` ui ON ui.id=l.unit_info "
                "WHERE l.`id` IN (SELECT `launch` FROM `report` WHERE `id` IN ("
                "SELECT `report` FROM `protocol_reports` WHERE `protocol`=%s) GROUP BY `launch`);", (row['id'],))

    run_time = ''
    unit_name = ''
    unit_descr = ''
    for row1 in cursor1:
        run_time = row1['end'].strftime('%m.%d.%Y')
        unit_name = row1['name']
        unit_descr = row1['descr']

    cursor1 = connection.cursor(dictionary=False)
    cursor1.execute("SELECT COUNT(*) FROM `protocol_reports` WHERE protocol=%s", (row['id'],))
    dev_count = cursor1.fetchall()[0][0]
    tbl.add_row(
        ('{}'.format(row['id']), 'class="cell-min-width"'),
        ('{}'.format(row['number']), 'class="cell-min-width"'),
        (run_time, 'class="cell-min-width"'),
        ('{}'.format(row['time']), 'class="cell-min-width"'),
        ('{}'.format(dev_count), 'class="cell-min-width"'),
        '<div title="{}">{}</div>'.format(row['descr'], row['name']),
        row['fio'],
        '<div title="{}">{}</div>'.format(unit_descr, unit_name),
        '{:.1f}°C {:.1f}% {:.1f}кПа'.format(row['t'],row['f'],row['p']),
        ('''<a href="getprotocol.py?id={id}" title="Открыть протокол в PDF"><img height=32 src="/icons/pdf.png"></a>
        '''.format(id=row['id']), 'class="cell-buttons"')
        )

html.add(html_blocks.PageNavigation('calibrprotocol.py?sort={}'.format(sort), page, page_count))
html.add(tbl)
html.add(html_blocks.PageNavigation('calibrprotocol.py?sort={}'.format(sort), page, page_count))
html.print()
