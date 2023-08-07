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

html = html_nero.HtmlBase("Редактирование группы стендов", 'stend.', 'Редактирование группы стендов')
html.add_js_files('/js/value_editor.js')
html.add_css_files('/css/value_editor.css')


connection = db.connect(**DB_CONFIG, database='stend_control_schema')
cursor = connection.cursor(dictionary=True)

group_id = form.getvalue('id', -1)
nav = form.getvalue('nav', '')

if group_id == -1 and nav == '':
    nav = 'first'

if group_id == -1:
    cursor.execute("SELECT MIN(id) AS id FROM `stend_control_schema`.`stend_groups`;")
    res = cursor.fetchone()
    if res: group_id = res['id']

if nav == 'first':
    #навигация
    cursor.execute( "SELECT `id` FROM `stend_control_schema`.`stend_groups` ORDER BY `id` limit 1;" )
    row = cursor.fetchone()
    if row:
        html_nero.HtmlBase.redirect('editstendgroup.py?id={}'.format(row['id']))
    else:
        html.add('''
        ОШИБКА: группа не найдена
        ''')

elif nav == 'last':
    #навигация
    cursor.execute( "SELECT `id` FROM `stend_control_schema`.`stend_groups` ORDER BY `id` DESC limit 1;" )
    row = cursor.fetchone()
    if row:
        html_nero.HtmlBase.redirect('editstendgroup.py?id={}'.format(row['id']))
    else:
        html.add('''
        ОШИБКА: группа не найдена
        ''')
elif nav == 'next':
    #навигация
    cursor.execute("SELECT `id` FROM `stend_control_schema`.`stend_groups` "
                   "WHERE `id`>%s "
                   "ORDER BY `id` limit 1;", (group_id,))
    row = cursor.fetchone()
    if row:
        html_nero.HtmlBase.redirect('editstendgroup.py?id={}'.format(row['id']))
    else:
        html.add('''
        ОШИБКА: группа не найдена
        ''')
elif nav == 'prev':
    #навигация
    cursor.execute("SELECT `id` FROM `stend_control_schema`.`stend_groups` "
                   "WHERE `id`<%s "
                   "ORDER BY `id` DESC limit 1;", (group_id,))
    row = cursor.fetchone()
    if row:
        html_nero.HtmlBase.redirect('editstendgroup.py?id={}'.format(row['id']))
    else:
        html.add('''
        ОШИБКА: группа не найдена
        ''')
else:
    #редактирование
    cursor.execute("SELECT `stend_id`,`description` FROM `stend_control_schema`.`stend_group_bind` "
                   "JOIN `stend_control_schema`.`stend_list` ON `stend`=`stend_id` "
                   "WHERE `group`=%s;", (group_id,))
    stends = cursor.fetchall()

    cursor.execute("SELECT `id`,`name` FROM `stend_control_schema`.`stend_groups` WHERE `id`=%s;", (group_id,))

    res = cursor.fetchall()
    if len(res):
        data = res[0]

        navi = html_blocks.ItemNavigation('editstendgroup.py', group_id, data['name'])
        html.add(navi)

        form = html_blocks.EditForm()
        stend_form = html_blocks.EditForm()

        form.add_info('ID', data['id'])

        if html.access_info['admin']:
            cursor.execute("SELECT `stend_id`,`description` FROM `stend_control_schema`.`stend_list` "
                   "WHERE `stend_id` NOT IN "
                   "(SELECT `stend` FROM `stend_control_schema`.`stend_group_bind` WHERE `group`=%s) "
                   ";", (group_id,))
            add_stends = [(row['stend_id'], '{} - {}'.format(row['stend_id'],row['description'])) for row in cursor.fetchall()]

            form.add_text_edit('Название', data['name'], 'name', '''{{cmd: 'modify_stend_group', id: {}}}'''.format(group_id))
            for stend in stends:
                stend_form.add_row('{}'.format(stend['stend_id']), None, None).add_text(stend['description']).add_button(
                    '<img height=24 src="/icons/btn_delete.png">',
                    '''{{cmd: 'modify_stend_group', id: {}, del: {}}}'''.format(group_id,stend['stend_id'])
                    )
            stend_form.add_new_row('', None, '''{{cmd: 'modify_stend_group', id: {}}}'''.format(group_id))\
                .add_combo_box('add', add_stends)
        else:
            form.add_info('Название', data['name'])

            for stend in stends:
                stend_form.add_info('{}'.format(stend['stend_id']), stend['description'])

        html.add(form)
        html.add('Стенды:')
        html.add(stend_form)
    else:
        html.add('''
    ОШИБКА: группа не найден
    ''')

html.print()
