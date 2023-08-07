#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from html_base import *
import client_tcp
import cgi, cgitb
import datetime

cgitb.enable()



form = cgi.FieldStorage()
stends = [int(v) for v in form.getlist('st')]
dt_from = form.getvalue('from', datetime.datetime.now().replace(hour=0, minute=0).strftime("%d.%m.%Y %H:%M"))
dt_to = form.getvalue('to', datetime.datetime.now().strftime("%d.%m.%Y %H:%M"))

add_css_file('/css/result_table_minimal_black.css')
print_head("Портал тестовых стендов Nero Electronics - перечень успешно проверенных устройств")

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
    cl.start_command('dev_protocol', dt_start=dt_from, dt_end=dt_to, stends=stends)
    request_id = cl.uuid()
    data = ''' {"a[]": "0|reportlist|0", "limit": 1000} '''
    add_script('''waitResultTable("{}", "progress", {});'''.format(request_id, data))
    add_script('''setInterval(function() {{ keepResult('{}');}}, 1000);'''.format(request_id))

add_script('''setStendTime('{}', '{}');'''.format(dt_from, dt_to))

print_end()