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
sort = form.getvalue('sort', 'launch-')
page = form.getvalue('page', '1')
mac = form.getvalue('mac', '')
try:
    condition = ' WHERE `mac`={}'.format(int(mac))
except:
    condition = ''

try:
    page = int(page)
except:
    page = 1

#sql sort-user sort-group sort-status
orders = {
    'number': 'id',
    'number-': 'id DESC',
    'launch': 'launch,place',
    'launch-': 'launch DESC,place',
    'mac': 'mac',
    'mac-': 'mac DESC',
}
order = orders.get(sort, orders['launch-'])

html = html_nero.HtmlBase("Перечень откалиброванных/поверенных приборов", 'calibration.calibrdevlist')

html.add('<form action="calibrdevlist.py"><input type="text" name="mac" value="{}"><button>Найти MAC</button></form>'.format(mac))

connection = db.connect(**DB_CONFIG, database='calibration')
cursor = connection.cursor(dictionary=False)
cursor.execute("SELECT COUNT(*) FROM calibration.report{};".format(condition))
dev_count = cursor.fetchall()[0][0]
page_size = 20
page_count = math.ceil(dev_count / page_size)

cursor = connection.cursor(dictionary=True, buffered=True)
cursor.execute("SELECT r.`id`,r.`launch`,r.`place`,r.`mac`,r.`result` FROM `report` r{} "
               "ORDER BY {} LIMIT {} OFFSET {};".format(condition, order, page_size, (page - 1) * page_size))


def sortlink(caption, key):
    fmt = '<a href="calibrdevlist.py?sort={}&page={}">{}{}</a>'
    if sort == key:
        return fmt.format(key + '-', page, '<img src="/icons/sort-up.png" height=16>', caption)
    elif sort == key + '-':
        return fmt.format(key, page, '<img src="/icons/sort-down.png" height=16>', caption)
    else:
        return fmt.format(key, page, '', caption)

tbl = html_blocks.Table()
tbl.caption = 'Перечень откалиброванных/поверенных приборов'
tbl.set_header(
              (sortlink('№ отчета', 'number'), 'class="cell-min-width"'),
              (sortlink('№ запуска', 'launch'), 'class="cell-min-width"'),
              ('Место', 'class="cell-min-width"'),
              ('Время', 'class="cell-min-width"'),
              ('Алгоритм', 'class="cell-min-width"'),
              (sortlink('MAC', 'mac'), 'class="cell-min-width"'),
              'Протокол',
              ('Результат', 'class="cell-min-width"'),
              ('','class="cell-buttons"'),
              )

n = page * 20
for row in cursor:
    cursor1 = connection.cursor(dictionary=True)
    cursor1.execute("SELECT `id`,`number`,`fio` FROM `protocol` WHERE `id` IN "
                       "(SELECT `protocol` FROM `protocol_reports` WHERE `report`=%s)", (row['id'],))
    protocol = ''
    for pr_row in cursor1:
        protocol = '<a href="getprotocol.py?id={}">{} - {}</a>'.format(pr_row['id'], pr_row['number'], pr_row['fio'])


    cursor1.execute("SELECT l.`end`, a.`name` FROM `launch` l JOIN `algoritm` a ON l.`algoritm`=a.`id` WHERE l.`id`=%s", (row['launch'],))
    inf_row = cursor1.fetchall()[0]

    tbl.add_row(
        ('<a href="calibrlog.py?id={id}">{id}</a>'.format(id=row['id']), 'class="cell-min-width"'),
        ('{}'.format(row['launch']), 'class="cell-min-width"'),
        ('{}'.format(row['place']), 'class="cell-min-width"'),
        ('{}'.format(inf_row['end']), 'class="cell-min-width"'),
        ('{}'.format(inf_row['name']), 'class="cell-min-width"'),
        ('<a href="calibrdevlist.py?mac={mac}">{mac}</a>'.format(mac=row['mac']), 'class="cell-min-width"'),
        protocol,
        (row['result'], 'class="cell-min-width"'),
        ('''<a href="calibrinfo.py?id={id}" title="Подробно"><img height=32 src="/icons/info.png"></a>
        '''.format(id=row['id']), 'class="cell-buttons"')
        )

html.add(html_blocks.PageNavigation('calibrdevlist.py?sort={}'.format(sort), page, page_count))
html.add(tbl)
html.add(html_blocks.PageNavigation('calibrdevlist.py?sort={}'.format(sort), page, page_count))
html.print()
