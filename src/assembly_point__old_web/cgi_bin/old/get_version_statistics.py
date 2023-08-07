#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import client_tcp
import cgi, cgitb
import datetime

from src.assembly_point__old_web.cgi_bin.old.html_base import add_css_file, add_css, print_head, print_period, \
    print_stend_list, add_script, print_end

cgitb.enable()



form = cgi.FieldStorage()
stends = [int(v) for v in form.getlist('st')]
dt_from = form.getvalue('from', datetime.datetime.now().replace(hour=0, minute=0).strftime("%d.%m.%Y %H:%M"))
dt_to = form.getvalue('to', datetime.datetime.now().strftime("%d.%m.%Y %H:%M"))

success_only = int(form.getvalue('success', '0'))
group_id = int(form.getvalue('group_id', '0'))

add_css_file('/css/result_table_minimal_black.css')
add_css('table.result { width: 0; }')
print_head("Портал тестовых стендов Nero Electronics - статистика версий")

#cgi.print_environ_usage() 

print('  <form action="get_version_statistics.py" target="_self">')

print('<fieldset><legend>Параметры</legend>')
print('<label><input type="checkbox" name="group_id" value="1" {}> Группировать по id</label><br>'.format('checked' if group_id else ''))
print('<label><input type="checkbox" name="success" value="1" {}> Только успешные проверки</label>'.format('checked' if success_only else ''))
print('</fieldset>')
print_period()
print_stend_list(stends)
print('   <p><input type="submit" value="Получить"></p>')
print('   </form>')

print('''<div ><progress id="progress" style="width: 100%" value="0.0" max="1.0">
Текст
</progress></div>''')

print('''   <div id="result"><div>''')

request_id = ''
if len(stends):
    cl = client_tcp.TCPClient()
    cl.start_command('version_statistics', stends, dt_from, dt_to, success_only, group_id)
    request_id = cl.uuid()
    add_script('''waitResultTable("{}", "progress", {{"uniform":1}});'''.format(request_id))

add_script('''setStendTime('{}', '{}');'''.format(dt_from, dt_to))
print_end()
