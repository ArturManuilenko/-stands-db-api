#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from shutil import copyfileobj
import sys
from exec.client_tcp import TCPClient
import cgi
import cgitb

cgitb.enable()

form = cgi.FieldStorage()
filename = form.getvalue('filename')
doc = form.getvalue('doc')
name = filename

if not filename:
    cmdid = form.getvalue('cmdid')
    cl = TCPClient(cmdid)
    data, files = cl.get_data()
    for item in files.items():
        name, filename = item
        break


if doc == '1':
    print('Content-Type: application/pdf')
else:
    print('Content-Description: File Transfer')
    print('Content-Type: application/octet-stream')
    print('Content-Disposition: attachment; filename={}'.format(name))
    print('Content-Transfer-Encoding: binary')
    print('Expires: 0')
    print('Cache-Control: must-revalidate')
    print('Pragma: public')
#print('Content-Length: {}'.format(os.path.getsize(tmppath + filename)))
print()
sys.stdout.flush()

cl = TCPClient()
tmppath = cl.temp_path()

bstdout = open(sys.stdout.fileno(), 'wb', closefd=False)
with open(tmppath + filename, 'rb') as f:
    copyfileobj(f, bstdout)
