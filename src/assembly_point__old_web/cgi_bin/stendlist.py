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
sort = form.getvalue('sort', 'id')

#sql sort-user sort-group sort-status
orders = {
    'id': 'stend_id',
    'id-': 'stend_id DESC',
    'type': 'device_id, stend_id',
    'type-': 'device_id DESC, stend_id',
}

order = orders.get(sort, orders['id'])

html = html_nero.HtmlBase("Список стендов", 'stend.stendlist')

connection = db.connect(**DB_CONFIG, database='stend_control_schema')
cursor = connection.cursor(dictionary=True)
#осталось маков по типам
cursor.execute('SELECT `id`,`mac_table`,`mac_start`,`mac_end`,`pool_table` FROM `device_type`;')
mac_rest = {}
for row in cursor.fetchall():
    addr_cursor = connection.cursor(dictionary=False)
    if row['pool_table'] is None:
        addr_cursor.execute('SELECT MAX(mac) FROM work.{}'.format(row['mac_table']))
        max_mac = addr_cursor.fetchall()[0][0]
        mac_rest[row['id']] = ('range', row['mac_start'], row['mac_end'], row['mac_end'] - max_mac)
    else:
        addr_cursor.execute('SELECT COUNT(`mac`) FROM `work`.`{}` WHERE `group`={} AND `mac` NOT IN (SELECT `mac` FROM `work`.`{}`);'.format(
            row['pool_table'], row['mac_start'], row['mac_table']))
        mac_rest[row['id']] = ('pool', row['mac_start'], row['mac_end'], addr_cursor.fetchall()[0][0])


cursor.execute("SELECT stend_id,description,generate,device_id,name,mac_start,mac_end "\
    "FROM stend_list INNER JOIN device_type ON stend_list.device_id=device_type.id ORDER BY {};".format(order))


def sortlink(caption, key):
    fmt = '<a href="stendlist.py?sort={}">{}{}</a>'
    if sort == key:
        return fmt.format(key + '-', '<img src="/icons/sort-up.png" height=16>', caption)
    elif sort == key + '-':
        return fmt.format(key, '<img src="/icons/sort-down.png" height=16>', caption)
    else:
        return fmt.format(key, '', caption)

tbl = html_blocks.Table()
tbl.caption = 'Перечень тестовых стендов'
tbl.set_header(
                (
                    sortlink('ID', 'id'),
                    'class="cell-min-width"'
                ),
                'Описание',
                sortlink('Тип', 'type'),
                (
                    '',
                    'class="cell-min-width"'
                ),
                (
                    'Адреса',
                    'class="cell-min-width"'
                ),
                (
                    'Доступно',
                    'class="cell-min-width"'
                ),
                (
                    '',
                    'class="cell-buttons"'
                ),
              )

for row in cursor:
    address_icon = '<img height=24 src="/icons/{}">'.format('add_plus.png' if row['generate'] else 'cancel.png')
    if row['device_id'] == 0:
        address_icon = ''
        addressing = ''
        mac_rest_s = '-'
        mac_rest_allert = False
    else:
        mr = mac_rest.get(row['device_id'])
        if mr[0] == 'pool':
            addressing = 'гр.{}'.format(mr[1])
        else:
            addressing = '{} - {}'.format(mr[1], mr[2])
        mac_rest_s = '{}'.format(mr[3])
        mac_rest_allert = mr[3] < 100

    tbl.add_row(
        ('{}'.format(row['stend_id']), 'class="cell-min-width"'),
        row['description'],
        row['name'],
        (address_icon, 'class="cell-min-width"'),
        (addressing, 'class="cell-min-width"'),
        (mac_rest_s, 'class="cell-min-width"{}'.format(' style="background:#FE9597"' if mac_rest_allert else '') ),
        ('<a href="editstend.py?id={id}" title="Редактировать"><img height=32 src="{icon}"></a>'.format(
            id=row['stend_id'], icon = '/icons/edit.png' if html.access_info['admin'] else '/icons/info.png'
            ), 'class="cell-buttons"')
        )


html.add(tbl)
html.print()
