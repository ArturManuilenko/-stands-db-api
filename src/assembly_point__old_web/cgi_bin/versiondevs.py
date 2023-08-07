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
sort = form.getvalue('sort', 'number-')
page = form.getvalue('page', '1')
model = form.getvalue('model', '0')
active = form.getvalue('active', '1')

try:
    page = int(page)
except:
    page = 1

try:
    model = int(model)
except:
    model = 0

#sql sort-user sort-group sort-status
orders = {
    'number': 'number',
    'number-': 'number DESC',
    'model': 'description',
    'model-': 'description DESC',
    'version': '`versions`.`id`,`version`,`variant`,`hard`',
    'version-': '`versions`.`id` DESC,`version` DESC,`variant` DESC,`hard` DESC',
    'open': 'open_time',
    'open-': 'open_time DESC',
    'close': 'close_time',
    'close-': 'close_time DESC',
}
order = orders.get(sort, orders['number-'])

cond = ''
if active == '1':
    cond = 'WHERE `allow`=1'
if model > 0:
    cond += '{} `versions`.`id`={}'.format(' AND' if len(cond) else 'WHERE ', model)

html = html_nero.HtmlBase("Контроль версий устройств", 'info.versiondevs')
html.add_js_files('/js/value_editor.js', '/js/commands.js')
html.add_css_files('/css/value_editor.css')

connection = db.connect(**DB_CONFIG, database='energomera')
cursor = connection.cursor(dictionary=False)
cursor.execute("SELECT COUNT(*) FROM `smarthome`.`versions` {};".format(cond))
record_count = cursor.fetchall()[0][0]
page_size = 20
page_count = math.ceil(record_count / page_size)

cursor = connection.cursor(dictionary=True)
cursor.execute("SELECT * "
                "FROM `smarthome`.`versions` JOIN `stend_control_schema`.`device_id_descr` ON `versions`.`id`=`device_id_descr`.`id` "
                "{} "
                "ORDER BY {} "
                "LIMIT {} OFFSET {};".format(
                    cond,
                    order,
                    page_size, (page - 1) * page_size
                    )
                )


def sortlink(caption, key):
    fmt = '<a href="versiondevs.py?sort={}&page={}&model={}&active={}">{}{}</a>'
    if sort == key:
        return fmt.format(key + '-', page, model, active, '<img src="/icons/sort-up.png" height=16>', caption)
    elif sort == key + '-':
        return fmt.format(key, page, model, active, '<img src="/icons/sort-down.png" height=16>', caption)
    else:
        return fmt.format(key, page, model, active, '', caption)

tbl = html_blocks.Table()
tbl.caption = 'Версии'

tbl.set_header(
              sortlink('№', 'number'),
              sortlink('Модель', 'model'),
              sortlink('Версия', 'version'),
              sortlink('Дата добавления', 'open'),
              sortlink('Дата блокировки', 'close'),
              ('', 'class="cell-min-width"'),
              ('','class="cell-buttons"'),
              )

for row in cursor:
    btn_lock = '''<button onclick="send_command({{cmd: 'lock_version', number: {}}});"><img height=24 src="/icons/btn_delete.png"></button>'''

    tbl.add_row(
        f'{row["number"]}',
        row['description'],
        f"{row['id']}.{row['version']}.{row['variant']}.{row['hard']}",
        f"{row['open_time']}",
        f"{row['close_time'] if row['close_time'] else '-'}",
        ('<img height=24 src="/icons/{}.png">'.format('allowed' if row['allow'] else 'cancel'), 'class="cell-min-width"'),
        (btn_lock.format(row['number']) if html.access_info['admin'] and row['allow'] else '', 'class="cell-buttons"')
        )


models = [(0, 'Все')]
cursor = connection.cursor(dictionary=True, buffered=True)
cursor.execute("SELECT `id`,`description` FROM `stend_control_schema`.`device_id_descr`;")
for row in cursor:
    models.append((row['id'], '({}) {}'.format(row['id'], row['description'])))

form = html_blocks.EditForm()
if html.access_info['admin']:
    form.add_text_edit('Добавить версию', '0.0.0.0', 'version', "{cmd: 'add_version'}")
form.add_info('Фильтр', '''
<form style="width:100%">
<label><input type="checkbox" name="active" value="0"{}>Показывать заблокированные</label>
<select name="model" >
{}
</select>
<input type="submit" value="Применить" style="float:right">
</form>
'''.format(
    ' checked' if active == '0' else '',
    '\n'.join(
    ['<option value="{}"{}>{}</option>'.format(id, ' selected' if id == model else '', name) for id,name in models]
    )));
html.add(form)

html.add(html_blocks.PageNavigation('versiondevs.py?sort={}&model={}&active={}'.format(sort,model, active), page, page_count))
html.add(tbl)
html.add(html_blocks.PageNavigation('versiondevs.py?sort={}&model={}&active={}'.format(sort,model, active), page, page_count))
html.print()
