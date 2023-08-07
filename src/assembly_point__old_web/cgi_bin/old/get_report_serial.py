#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import client_tcp
import cgi, cgitb

from src.assembly_point__old_web.cgi_bin.old.html_base import add_css_file, print_head, add_script, print_end

cgitb.enable()

form = cgi.FieldStorage()
serial = form.getvalue('serial')
add_css_file('/css/result_table_minimal_black.css')
print_head("Портал тестовых стендов Nero Electronics - полный отчет")

print('  <form target="_self">')
print('<fieldset><legend>Параметры</legend>')

print('<p>Серийный номер процессора: <input name="serial" type="text" min=0 value={}></p>'.format(serial if serial else 0))

print('</fieldset>')
print('   <p><input type="submit" value="Получить"></p>')
print('   </form>')

print('''<div ><progress id="progress" style="width: 100%" value="0.0" max="1.0">
Текст
</progress></div>''')


request_id = ''
print('<pre id="result">')
print('</pre>')
if serial:
    cl = client_tcp.TCPClient()
    cl.start_command('report_condition', serial=serial)
    request_id = cl.uuid()
    data = ''' {"col[]": [7]} '''
    add_script('''waitResultTable("{}", "progress", {});'''.format(request_id,data))
    
print_end()
