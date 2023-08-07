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

html = html_nero.HtmlBase("Редактирование модификации", 'info.editmod', 'Редактирование модификации')

html.add_js_files('/js/value_editor.js')
html.add_css_files('/css/value_editor.css')


connection = db.connect(*DB_CONFIG, database='stend_control_schema')
cursor = connection.cursor(dictionary=True)

mod_id = form.getvalue('id', -1)
nav = form.getvalue('nav', '')

if mod_id == -1 and nav == '':
    nav = 'first'

if mod_id == -1:
    cursor.execute("SELECT MIN(id) AS id FROM modification_list;")
    res = cursor.fetchone()
    if res:
        stend_id = res['id']

if nav == 'first':
    #навигация
    cursor.execute("SELECT id FROM modification_list ORDER BY id limit 1;")
    row = cursor.fetchone()
    if row:
        html_nero.HtmlBase.redirect('editmod.py?id={}'.format(row['id']))
    else:
        html.add('''
        ОШИБКА: модификация не найдена
        ''')

elif nav == 'last':
    #навигация
    cursor.execute( "SELECT id FROM modification_list ORDER BY id DESC limit 1;" )
    row = cursor.fetchone()
    if row:
        html_nero.HtmlBase.redirect('editmod.py?id={}'.format(row['id']))
    else:
        html.add('''
        ОШИБКА: модификация не найдена
        ''')
elif nav == 'next':
    #навигация
    cursor.execute("SELECT id FROM modification_list "
                   "WHERE id>%s "
                   "ORDER BY id limit 1;", (mod_id,))
    row = cursor.fetchone()
    if row:
        html_nero.HtmlBase.redirect('editmod.py?id={}'.format(row['id']))
    else:
        html.add('''
        ОШИБКА: модификация не найдена
        ''')
elif nav == 'prev':
    #навигация
    cursor.execute("SELECT id FROM modification_list "
                   "WHERE id<%s "
                   "ORDER BY id DESC limit 1;", (id,))
    row = cursor.fetchone()
    if row:
        html_nero.HtmlBase.redirect('editmod.py?id={}'.format(row['id']))
    else:
        html.add('''
        ОШИБКА: модификация не найдена
        ''')
else:
    #редактирование
    cursor.execute("SELECT id,name,model,description FROM modification_list WHERE id=%s;", (mod_id,))

    res = cursor.fetchall()
    if len(res):
        data = res[0]

        navi = html_blocks.ItemNavigation('editmod.py', mod_id, data['description'])
        html.add(navi)

        form = html_blocks.EditForm()
        form.add_info('ID', data['id'])

        if html.access_info['admin']:
            cmd = '''{{cmd: 'modify_mod', id: {}}}'''.format(mod_id)

            form.add_text_edit('Модификация', data['name'], 'name', cmd)
            form.add_text_edit('Модель', data['model'], 'model', cmd)
            form.add_text_edit('Описание', data['description'], 'descr', cmd)
        else:
            form.add_info('Модификация', data['name'])
            form.add_info('Модель', data['model'])
            form.add_info('Описание', data['description'])


        html.add(form)
    else:
        html.add('''
    ОШИБКА: стенд не найден
    ''')

html.print()
