#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import client_tcp

import cgi, cgitb

cgitb.enable()
print('Content-Type: text/html\n\n')


def fun_null(*args):
    return '!'


def fun_reportlist(id_list):
    if type(id_list) is int:
        id_list = [id_list]
    l=['id={}'.format(id) for id in id_list]
    return "get_report_text.py?{}".format('&'.join(l))


def fun_byserial(serial):
    return "get_report_serial.py?serial={}".format(serial)


commands = {
    'reportlist': fun_reportlist,
    'byserial': fun_byserial,
    }

a_list = {}


def parse_a(value):
    parts = value.split('|')
    params = [int(v) for v in parts[2].split(',')]
    a_list[int(parts[0])] = (commands.get(parts[1], fun_null), params)


def print_header(row):    
    print('<tr>')
    w = ' width="{}%"'.format(100.0/len(row)) if uniform else ''
    for col in cols:
        print('<th{}>{}</th>'.format(w, row[col]))
    print('</tr>')


def print_row(row):
    print('<tr>')
    for col in cols:
        a = a_list.get(col)
        if a:
            params = tuple([row[i] for i in a[1]])
            print('<td><a target="_blank" href="{}">{}</a></td>'.format(a[0](*params), row[col]))
        else:
            print('<td>{}</td>'.format(row[col]))
    print('</tr>')


def print_limit_overflow(row):
    print('<tr>')
    print('<td colspan="{}">Превышен лимит выдачи данных, показаны не все значения. Измените параметры запроса.</td>'.format(len(row)))
    print('</tr>')


form = cgi.FieldStorage()
form_id = form.getvalue('id')

descr = form.getlist('descr')
a = form.getlist('a[]')# 1|reportlist|2 column|function|columns_to_param
cols = [int(v) for v in form.getlist('col[]')]
uniform = form.getvalue('uniform')
limit = int(form.getvalue('limit', '100000'))

for val in a:
    parse_a(val)
    
cl = client_tcp.TCPClient(form_id)
data, files = cl.get_data()

for file in files.values():
    print(''' <a href='{}'>Скачать файл: {}</a>'''.format('download.py?filename=' + file, file))
    print('<br>')

if len(cols) == 0:
    cols = list(range(len(data['header'])))

print('<table class="result">')
print('<thead>')
print_header(data['header'])
print('</thead>')

print('<tbody>')
for n, r in enumerate(data['rows']):
    if n > limit:
        print_limit_overflow(r)
        break
    else:
        print_row(r)
print('</tbody>')

print('<tfoot>')
for r in data.get('footer', []):
    print_row(r)
print('<tfoot>')

print('</table>')
