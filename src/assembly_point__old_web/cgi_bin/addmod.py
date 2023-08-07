#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cgi
import cgitb
import html_nero
import html_blocks

cgitb.enable()

form = cgi.FieldStorage()

html = html_nero.HtmlBase("Добавление модификации", 'info.addmod', 'Добавление модификации')
html.add_js_files('/js/value_editor.js')
html.add_css_files('/css/value_editor.css')



if html.access_info['admin']:
    #редактирование

    cmd = '''{cmd: 'modify_mod'}'''

    form = html_blocks.EditForm(group_apply = True, command = cmd)

    form.add_row('Модификация').add_text_edit('name', 'MM')
    form.add_row('Модель').add_text_edit('model', 'неизвестное устройство')
    form.add_row('Описание').add_text_edit('descr', '?')

    form.add_group_buttons(cmd, btn_apply ='Создать')

    html.add(form)

html.print()
