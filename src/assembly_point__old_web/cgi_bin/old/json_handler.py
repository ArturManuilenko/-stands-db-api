#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import client_tcp
import json

import cgi, cgitb

cgitb.enable()
result = {}

form = cgi.FieldStorage()
cmd = form.getvalue('cmd')
id = form.getvalue('id')

if cmd == 'progress':
    cl = client_tcp.TCPClient(id)
    progress, ready = cl.check_progress()
    result['value'] = progress
    result['ready'] = ready
elif cmd == 'result_html':
    cl = client_tcp.TCPClient(id)
elif cmd == 'keep':
    cl = client_tcp.TCPClient(id)
    cl.keep()

print('Content-Type: application/json\n\n')
print(json.dumps(result))
