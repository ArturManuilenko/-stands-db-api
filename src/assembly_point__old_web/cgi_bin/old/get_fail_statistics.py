#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import client_tcp
import cgi, cgitb
import datetime

from src.assembly_point__old_web.cgi_bin.old.html_base import add_css_file, print_head, print_period, print_stend_list, \
    add_script, print_end

cgitb.enable()



form = cgi.FieldStorage()
stends = [int(v) for v in form.getlist('st')]
dt_from = form.getvalue('from', datetime.datetime.now().replace(hour=0, minute=0).strftime("%d.%m.%Y %H:%M"))
dt_to = form.getvalue('to', datetime.datetime.now().strftime("%d.%m.%Y %H:%M"))

add_css_file('/css/result_table_minimal_black.css')
print_head("Портал тестовых стендов Nero Electronics - статистика ошибок")

print('  <form target="_self">')

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
    cl.start_command('fail_statistics', stends, dt_from, dt_to)
    request_id = cl.uuid()
    data = ''' {"col[]": [0,1], "a[]": "1|reportlist|2"} '''
    add_script('''waitResultTable("{}", "progress", {});'''.format(request_id, data))

add_script('''setStendTime('{}', '{}');'''.format(dt_from, dt_to))
print_end()
