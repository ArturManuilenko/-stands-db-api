#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import client_tcp
import cgi, cgitb

from src.assembly_point__old_web.cgi_bin.old.html_base import add_css_file, print_head, print_stend_list, add_script, \
    print_end

cgitb.enable()



form = cgi.FieldStorage()
stends = [int(v) for v in form.getlist('st')]
ftypes = form.getlist('ftype')
if not len(ftypes):
    ftypes.append('D')

add_css_file('/css/result_table_minimal_black.css')
print_head("Портал тестовых стендов Nero Electronics - назначенные версии прошивок")

print('  <form target="_self">')

print('<fieldset><legend>Тип</legend>')
print('<label><input type="checkbox" name="ftype" value="B" {}> Бутлоадер</label>'.format('checked' if 'B' in ftypes else ''))
print('<label><input type="checkbox" name="ftype" value="S" {}> Стенд</label>'.format('checked' if 'S' in ftypes else ''))
print('<label><input type="checkbox" name="ftype" value="D" {}> ВПО устройства</label>'.format('checked' if 'D' in ftypes else ''))
print('</fieldset>')


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
    cl.start_command('stend_versions', stends, ftypes)
    request_id = cl.uuid()

    add_script('''waitResultTable("{}", "progress");'''.format(request_id))
print_end()
