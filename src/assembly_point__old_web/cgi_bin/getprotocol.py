#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cgi
import cgitb
import html_nero
import html_blocks

import mysql.connector as db
import mysql.connector.cursor
import time
from exec.client_tcp import TCPClient

cgitb.enable()

form = cgi.FieldStorage()
id = form.getvalue('id')

if type(id) is list:
    ids = [int(i) for i in id]
else:
    ids = [int(id)]

html = html_nero.HtmlBase("Формирование протокола поверки", 'report.getprotocol', 'Формирование протокола поверки')
html.add_js_files('/js/stend-script_v2.js')

cl = TCPClient()
cl.start_command('protocol_verification', ids=ids)
request_id = cl.uuid()

html.add_script('''
window.onload = function(){{
    waitFile('{request_id}','progress','result');
}};
'''.format(request_id=request_id))
html.add('''<br>Формируется протокол, подождите...<br><a id="result"></a><div ><progress id="progress" style="width: 100%" value="0.0" max="1.0">
Текст
</progress></div>''')
html.print()
