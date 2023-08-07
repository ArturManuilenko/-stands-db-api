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
sort = form.getvalue('sort', 'date')
page = form.getvalue('page', '0')
try:
    page = int(page)
except:
    page = 0

#sql sort-user sort-group sort-status
orders = {
    'date': 'end',
    'date-': 'end DESC',
    'unit': 'u.name, end',
    'unit-': 'u.name DESC, end',
    'alg': 'a.name, end',
    'alg-': 'a.name DESC, end',
}
order = orders.get(sort, orders['date-'])

html = html_nero.HtmlBase("Перечень откалиброванных/поверенных приборов", 'calibration.calibrlist')

if html.access_info['admin']:
    html.add_js_files('/js/commands.js')

connection = db.connect(**DB_CONFIG, database='calibration')
cursor = connection.cursor(dictionary=True, buffered=True)
cursor.execute("SELECT l.id,l.start,l.end,l.stage_count as lstages,a.name as alg,a.id as alg_id,a.stage_count as stages,u.name as unit_name,"
    "(SELECT COUNT(id) FROM `report` WHERE launch=l.id AND result='000-ok') as success,"
    "(SELECT COUNT(id) FROM `report` WHERE launch=l.id) as devs "
    "FROM `launch` l JOIN `algoritm` a ON l.algoritm=a.id JOIN `unit` u ON l.unit=u.id ORDER BY {} LIMIT 20 OFFSET {};".format(order, page*20))


def sortlink(caption, key):
    fmt = '<a href="calibrlist.py?sort={}&page={}">{}{}</a>'
    if sort == key:
        return fmt.format(key + '-', page, '<img src="/icons/sort-up.png" height=16>', caption)
    elif sort == key + '-':
        return fmt.format(key, page, '<img src="/icons/sort-down.png" height=16>', caption)
    else:
        return fmt.format(key, page, '', caption)


tbl = html_blocks.Table()
tbl.caption = 'Перечень запусков калибровки/поверки приборов'
tbl.set_header(
              ('№', 'class="cell-min-width"'),
              (sortlink('Время', 'date'), 'class="cell-min-width"'),
              sortlink('Установка', 'unit'),
              sortlink('Алгоритм', 'alg'),
              ('Успешно', 'class="cell-min-width"'),
              ('Этапы', 'class="cell-min-width"'),
              'Протоколы',
              ('','class="cell-buttons"'),
              )


icon = '/icons/edit.png' if html.access_info['admin'] else '/icons/info.png'
n = page * 20
for row in cursor:
    n += 1
    if row['alg_id'] == 0 or row['success'] == 0 or row['lstages'] < row['stages']:
        protocols = 'недоступно'
    else:
        protos = []
        cursor1 = connection.cursor(dictionary=True)
        cursor1.execute("SELECT `id`,`number` FROM `protocol` WHERE `id` IN "
                       "(SELECT `protocol` FROM `protocol_reports` WHERE `report` IN "
                       "(SELECT `id` FROM `report` WHERE `launch`=%s) "
                       "GROUP BY protocol)", (row['id'],))

        for protorow in cursor1:
            protos.append('<a href="getprotocol.py?id={}">{}</a>'.format(protorow['id'], protorow['number']))
        protocols = ' '.join(protos)
        if html.access_info['protocol']:
            protocols += ' <a href="addprotocol.py?launch={id}" title="Зарегистрировать новый протокол">'\
        '<img height=16 src="/icons/add_plus.png"></a>'.format(id=row['id'])

    tbl.add_row(
        ('{}'.format(n), 'class="cell-min-width"'),
        (row['end'], 'class="cell-min-width"'),
        str(row['unit_name']),
        str(row['alg']),
        ('{}/{}'.format(row['success'], row['devs']), 'class="cell-min-width"'),
        ('{}/{}'.format(row['lstages'], row['stages']), 'class="cell-min-width"'),
        protocols,
        ('''<a href="editlaunch.py?id={id}" title="Подробно"><img height=32 src="{icon}"></a>
        '''.format(id=row['id'], icon=icon), 'class="cell-buttons"')
        )


html.add(tbl)
html.print()
