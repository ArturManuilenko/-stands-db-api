#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import client_tcp
import cgi, cgitb

cgitb.enable()

form = cgi.FieldStorage()
res_format = form.getvalue('format', 'plain')
ids = [int(v) for v in form.getlist('id')]

print('Content-Type: text/plain; charset=UTF-8')
print('')

cl = client_tcp.TCPClient()
cl.start_command('report', ids)
request_id = cl.uuid()

ready = False
while not ready:
    progress, ready = cl.check_progress()

data, files = cl.get_data()
print(data)
cl.kill()
