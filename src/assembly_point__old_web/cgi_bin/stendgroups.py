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
sort = form.getvalue('sort', 'number-')

html = html_nero.HtmlBase("Группы стендов", 'stend.stendgroups')
html.add_js_files('/js/value_editor.js', '/js/commands.js')
html.add_css_files('/css/value_editor.css')

connection = db.connect(**DB_CONFIG, database='energomera')
cursor = connection.cursor(dictionary=True)
cursor.execute("SELECT `id`,`name` FROM `stend_control_schema`.`stend_groups`;")
groups = cursor.fetchall()

tbl = html_blocks.Table()
tbl.caption = 'Группы стендов'

tbl.set_header(
              'Группа',
              'Стенды',
              ('', 'class="cell-buttons"'),
              )

cursor = connection.cursor(dictionary=False)
buttons = '''<a href="editstendgroup.py?id={}"><img height=24 src="/icons/edit.png"></a>
    <button onclick="send_command({{cmd: 'del_stend_group', id: {}}});"><img height=24 src="/icons/btn_delete.png"></button>
    '''
for row in groups:
    cursor.execute("SELECT `stend_id`,`description` FROM `stend_control_schema`.`stend_group_bind` "
                   " JOIN `stend_control_schema`.`stend_list` ON `stend`=`stend_id`"
                   "WHERE `group`=%s;", (row['id'],))
    stends = ['<span title="{}">{}</span>'.format(id,descr) for id,descr in cursor]

    tbl.add_row(
        row['name'],
        '; '.join(stends),
        (buttons.format(row['id'], row['id']) if html.access_info['admin'] else '', 'class="cell-buttons"')
        )

if html.access_info['admin']:
    form = html_blocks.EditForm()
    form.add_text_edit('Добавить группу', '', 'name', "{cmd: 'add_stend_group'}")
    html.add(form)

html.add(tbl)
html.print()
