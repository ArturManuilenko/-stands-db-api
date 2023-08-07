#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cgi, cgitb
import html_nero
import html_blocks

import mysql.connector as db
import mysql.connector.cursor
import time
import math

import urllib.parse
import datetime

from src.assembly_point__old_web.env import DB_CONFIG

cgitb.enable()

form = cgi.FieldStorage()
sort = form.getvalue('sort', 'time-')
page = form.getvalue('page', '1')

s_from = form.getvalue('from', '01.01.{} 00:00'.format(datetime.datetime.now().year))
s_to = form.getvalue('to', datetime.datetime.now().strftime('%d.%m.%Y %H:%M'))
try:
    page = int(page)
except:
    page = 1

dt_from = datetime.datetime.strptime(s_from, '%d.%m.%Y %H:%M')
dt_to = datetime.datetime.strptime(s_to, '%d.%m.%Y %H:%M')

#sql sort-user sort-group sort-status
orders = {
    'time': 'date',
    'time-': 'date DESC',
}
order = orders.get(sort, orders['time-'])
date_param = 'from={}&to={}'.format(urllib.parse.quote(s_from),urllib.parse.quote(s_to))

html = html_nero.HtmlBase("Отчет программирования счетчиков Энергомеры", 'report.energomerareport')

html.add_js_files('/js/jquery.datetimepicker.full.min.js', '/stend_time.js')
html.add_css_files('/css/jquery.datetimepicker.min.css')

connection = db.connect(**DB_CONFIG, database='energomera')
cursor = connection.cursor(dictionary=False)
cursor.execute("SELECT COUNT(*) FROM `firm` WHERE `date`>=%s AND `date`<%s AND `rep`=0 AND `new`=1 AND `result`=1;",
               (dt_from, dt_to)
               )
record_count = cursor.fetchall()[0][0]
page_size = 20
page_count = math.ceil(record_count / page_size)


cursor = connection.cursor(dictionary=True, buffered=True)
cursor.execute("SELECT `date`,`stend`,`mac`,`serial`,`version`,`result`,`rep`,`new`,`mail` FROM `firm` "
                "JOIN `mail` ON `mail`.`id`=`firm`.`mail` "
                "WHERE `date`>=%s AND `date`<%s AND `rep`=0 AND `new`=1 AND `result`=1 "
                "ORDER BY {} LIMIT {} OFFSET {};".format(order, page_size, (page - 1) * page_size),
                (dt_from, dt_to)
                )

def sortlink(caption, key):
    fmt = '<a href="energomerareport.py?sort={}&page={}&{}">{}{}</a>'
    if sort == key:
        return fmt.format(key + '-', page, date_param, '<img src="/icons/sort-up.png" height=16>', caption)
    elif sort == key + '-':
        return fmt.format(key, page, date_param, '<img src="/icons/sort-down.png" height=16>', caption)
    else:
        return fmt.format(key, page, date_param, '', caption)

tbl = html_blocks.Table()
tbl.caption = 'Отчет программирования ({} новых приборов)'.format(record_count)

["DATETIME (GMT)", "STEND", "MAC", "SERIAL", "VERSION", "RESULT", "DEVICE"]
tbl.set_header(
              (sortlink('Дата (GMT)', 'time'), 'class="cell-min-width"'),
              ('Стенд', 'class="cell-min-width"'),
              ('Адрес', 'class="cell-min-width"'),
              ('Версия', 'class="cell-min-width"'),
              'Серийный номер контроллера',
              ('Результат', 'class="cell-min-width"'),
              ('','class="cell-buttons"'),
              )

for row in cursor:
    tbl.add_row(
        ('{}'.format(row['date']), 'class="cell-min-width"'),
        (row['stend'], 'class="cell-min-width"'),
        ('{}'.format(row['mac']), 'class="cell-min-width"'),
        (row['version'], 'class="cell-min-width"'),
        row['serial'],
        ('OK NEW', 'class="cell-min-width"'),
        ('''<a href="getmail.py?id={id}" title="Открыть письмо"><img height=24 src="/icons/mail.png"></a>
        '''.format(id=row['mail']), 'class="cell-buttons"')
        )

html.add(html_blocks.PeriodPicker(s_from, s_to, {'sort':sort}))
html.add('<a href="getenergomera.py?{}"><div class="button"><img height=32 src="/icons/excel.png">получить отчет Excel<div></a>'.format(date_param))
html.add(html_blocks.PageNavigation('energomerareport.py?sort={}&{}'.format(sort,date_param), page, page_count))
html.add(tbl)
html.add(html_blocks.PageNavigation('energomerareport.py?sort={}&{}'.format(sort,date_param), page, page_count))
html.print()
