#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import html_base
import client_tcp
import json
from shutil import copyfileobj
import sys
import os

import cgi, cgitb

cgitb.enable()

form = cgi.FieldStorage()
filename = form.getvalue('filename')

'''
print("Content-type: application/octet-stream")
print("Content-Disposition: attachment; filename={}".format(filename))
'''
print('Content-Description: File Transfer')
print('Content-Type: application/octet-stream')
print('Content-Disposition: attachment; filename={}'.format(filename))
print('Content-Transfer-Encoding: binary')
print('Expires: 0')
print('Cache-Control: must-revalidate')
print('Pragma: public')
#print('Content-Length: {}'.format(os.path.getsize(tmppath + filename)))
print()
sys.stdout.flush()

cl = client_tcp.TCPClient()
tmppath = cl.temp_path()

bstdout = open(sys.stdout.fileno(), 'wb', closefd=False)
with open(tmppath + filename, 'rb') as f:
    copyfileobj(f, bstdout)
