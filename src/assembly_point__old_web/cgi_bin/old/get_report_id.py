#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import client_tcp
import cgi, cgitb

from src.assembly_point__old_web.cgi_bin.old.html_base import print_head, print_end

cgitb.enable()

form = cgi.FieldStorage()
ids = [int(v) for v in form.getlist('id')]

print_head("Портал тестовых стендов Nero Electronics - полный отчет")

print('  <form target="_self">')
print('<fieldset><legend>Параметры</legend>')
if len(ids):
    for id in ids:
        print('<p>Номер отчета: <input name="id" type="number" min=1 value={}></p>'.format(id))
else:
    print('Номер отчета: <input name="id" type="number" min=1 value=1>')
print('</fieldset>')
print('   <p><input type="submit" value="Получить"></p>')
print('   </form>')

request_id = ''
print('<pre>')
if len(ids):
    cl = client_tcp.TCPClient()
    cl.start_command('report', ids)
    request_id = cl.uuid()
    ready = False
    while not ready:
        progress, ready = cl.check_progress()
    data, files = cl.get_data()
    print(data)
    cl.kill()

print('</pre>')
print_end()
