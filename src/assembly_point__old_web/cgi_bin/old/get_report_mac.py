#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from html_base import *
import client_tcp
import cgi, cgitb

cgitb.enable()

form = cgi.FieldStorage()
mac = form.getvalue('mac')
add_css_file('/css/result_table_minimal_black.css')
print_head("Портал тестовых стендов Nero Electronics - полный отчет")

print('  <form target="_self">')
print('<fieldset><legend>Параметры</legend>')

print('<p>MAC адрес: <input name="mac" type="number" min=0 value={}></p>'.format(mac if mac else 0))

print('</fieldset>')
print('   <p><input type="submit" value="Получить"></p>')
print('   </form>')

print('''<div ><progress id="progress" style="width: 100%" value="0.0" max="1.0">
Текст
</progress></div>''')


request_id = ''
print('<pre id="result">')
print('</pre>')
if mac:
    cl = client_tcp.TCPClient()
    cl.start_command('report_condition', mac=int(mac))
    request_id = cl.uuid()
    data = ''' {"col[]": [7]} '''
    add_script('''waitResultTable("{}", "progress", {});'''.format(request_id, data))
    
print_end()
