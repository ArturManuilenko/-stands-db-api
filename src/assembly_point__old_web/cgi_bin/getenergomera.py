#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cgi
import cgitb
import html_nero

import datetime
from exec.client_tcp import TCPClient

cgitb.enable()

form = cgi.FieldStorage()
s_from = form.getvalue('from', '2000-01-01 00:00:00')
s_to = form.getvalue('to', '2099-01-01 00:00:00')

dt_from = datetime.datetime.strptime(s_from, '%d.%m.%Y %H:%M')
dt_to = datetime.datetime.strptime(s_to, '%d.%m.%Y %H:%M')

html = html_nero.HtmlBase("Формирование отчета стендов программарования счетчиков Энергомеры",
                          'report.getenergomera', 'Формирование отчета')
html.add_js_files('/js/stend-script_v2.js')

cl = TCPClient()
cl.start_command('energomera_report', dt_from=dt_from.strftime('%Y-%m-%d %H:%M:%S'), dt_to=dt_to.strftime('%Y-%m-%d %H:%M:%S'))
request_id = cl.uuid()

html.add_script('''
window.onload = function(){{
    waitFile('{request_id}','progress','result',0);
}};
'''.format(request_id=request_id))
html.add('''<br>Формируется отчет, подождите...<br><a id="result"></a><div ><progress id="progress" style="width: 100%" value="0.0" max="1.0">
Текст
</progress></div>''')
html.print()
