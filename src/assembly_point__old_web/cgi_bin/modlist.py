#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cgi
import cgitb
import html_nero
import html_blocks

import mysql.connector as db
import mysql.connector.cursor
import time

from src.assembly_point__old_web.env import DB_CONFIG

cgitb.enable()

form = cgi.FieldStorage()
sort = form.getvalue('sort', 'name')

#sql sort-user sort-group sort-status
orders = {
    'name': 'name',
    'name-': 'name DESC',
    'model': 'model, name',
    'model-': 'model DESC, name',
}
order = orders.get(sort, orders['name'])

html = html_nero.HtmlBase("Список модификаций приборов", 'info.modlist')

if html.access_info['admin']:
    html.add_js_files('/js/commands.js')

connection = db.connect(**DB_CONFIG, database='stend_control_schema')
cursor = connection.cursor(dictionary=True)
cursor.execute("SELECT id,name,model,description "\
    "FROM modification_list ORDER BY {};".format(order))

def sortlink(caption, key):
    fmt = '<a href="modlist.py?sort={}">{}{}</a>'
    if sort == key:
        return fmt.format(key + '-', '<img src="/icons/sort-up.png" height=16>', caption)
    elif sort == key + '-':
        return fmt.format(key, '<img src="/icons/sort-down.png" height=16>', caption)
    else:
        return fmt.format(key, '', caption)

if html.access_info['admin']:
    html.add('<a href="addmod.py">Добавить модификацию</a><br><br>')

tbl = html_blocks.Table()
tbl.caption = 'Перечень модификаций приборов'
tbl.set_header(
              ('№', 'class="cell-min-width"'),
              (sortlink('Модификация', 'name'), 'class="cell-min-width"'),
              sortlink('Модель', 'model'),
              'Описание',
              ('', 'class="cell-buttons"'),
              )


bdel = '''<a href="" title="Удалить" onclick="delMod({id})"><img height=32 src="/icons/btn_delete.png"></a>''' if html.access_info['admin'] else ''
icon = '/icons/edit.png' if html.access_info['admin'] else '/icons/info.png'
n = 0
for row in cursor:
    n += 1
    tbl.add_row(
        ('{}'.format(n), 'class="cell-min-width"'),
        (row['name'], 'class="cell-min-width"'),
        row['model'],
        row['description'],
        ('''<a href="editmod.py?id={id}" title="Редактировать"><img height=32 src="{icon}"></a>
        {bdel}'''.format(bdel=bdel, id=row['id'], icon = icon), 'class="cell-buttons"')
        )


html.add(tbl)
html.print()
