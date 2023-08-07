#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cgi
import cgitb
import html_nero
import html_blocks

import mysql.connector as db
import mysql.connector.cursor
import time
import math

from src.assembly_point__old_web.env import DB_CONFIG

cgitb.enable()

form = cgi.FieldStorage()
sort = form.getvalue('sort', 'date-')
page = form.getvalue('page', '1')
try:
    page = int(page)
except:
    page = 1
unit = form.getvalue('unit', '0')
try:
    unit = int(unit)
except:
    unit = 0

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

filter = '' if unit == 0 else ' WHERE l.unit={}'.format(unit)

html = html_nero.HtmlBase("Перечень запусков калибровки/поверки приборов", 'calibration.calibrlist')

if html.access_info['admin']:
    html.add_js_files('/js/commands.js')

connection = db.connect(**DB_CONFIG, database='calibration')

cursor = connection.cursor(dictionary=False)
cursor.execute("SELECT COUNT(*) FROM `launch` l {};".format(filter))
dev_count = cursor.fetchall()[0][0]
page_size = 20
page_count = math.ceil(dev_count / page_size)

cursor = connection.cursor(dictionary=True, buffered=True)
cursor.execute("SELECT l.id,l.start,l.end,l.stage_count as lstages,a.name as alg, a.id as alg_id,a.stage_count as stages,u.name as unit_name,"
    "(SELECT COUNT(id) FROM `report` WHERE launch=l.id AND result='000-ok') as success,"
    "(SELECT COUNT(id) FROM `report` WHERE launch=l.id) as devs "
    "FROM `launch` l JOIN `algoritm` a ON l.algoritm=a.id JOIN `unit` u ON l.unit=u.id {} ORDER BY {} LIMIT {} OFFSET {};".format(
        filter, order, page_size, (page - 1) * page_size))


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


n = (page-1) * 20
for row in cursor:
    n+=1
    if row['success'] == 0 or row['lstages'] < row['stages']:
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
        if html.access_info['protocol'] and row['alg_id'] > 0:
            protocols += ' <a href="addprotocol.py?launch={id}" title="Зарегистрировать новый протокол">'\
        '<img height=16 src="/icons/add_plus.png"></a>'.format(id=row['id'])

    tbl.add_row(
        ('{}'.format(n), 'class="cell-min-width"'),
        (row['end'], 'class="cell-min-width"'),
        str(row['unit_name']),
        str(row['alg']),
        ('{}/{}'.format(row['success'],row['devs']), 'class="cell-min-width"'),
        ('{}/{}'.format(row['lstages'],row['stages']), 'class="cell-min-width"'),
        protocols,
        ('''<a href="calibrinfo.py?launch={id}" title="Редактировать"><img height=32 src="/icons/info.png"></a>
        '''.format(id=row['id']), 'class="cell-buttons"')
        )


units = [(0, 'Все')]
cursor = connection.cursor(dictionary=True, buffered=True)
cursor.execute("SELECT `id`,`name` FROM `calibration`.`unit` WHERE `id`!=0 AND `name` IS NOT NULL;")
for row in cursor:
    units.append((row['id'], '({}) {}'.format(row['id'], row['name'])))
form = html_blocks.EditForm()
form.add_info('Фильтр', '''
<form style="width:100%">
<select name="unit" >
{}
</select>
<input type="submit" value="Применить" style="float:right">
</form>
'''.format(
    '\n'.join(
    ['<option value="{}"{}>{}</option>'.format(id, ' selected' if unit_id == unit else '', name) for unit_id, name in units]
    )));
html.add(form)
html.add(html_blocks.PageNavigation('calibrlist.py?sort={}&unit={}'.format(sort, unit), page, page_count))
html.add(tbl)
html.add(html_blocks.PageNavigation('calibrlist.py?sort={}&unit={}'.format(sort, unit), page, page_count))

html.print()
