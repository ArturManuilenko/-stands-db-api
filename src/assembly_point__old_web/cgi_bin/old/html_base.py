#!/usr/bin/env python3

import client_tcp

import codecs
import sys
import mysql.connector as db
from collections import OrderedDict

from src.assembly_point__old_web.env import DB_CONFIG

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

js_files = OrderedDict()


def add_script_file(src):
    js_files[src] = None

js_scripts = OrderedDict()


def add_script(src):
    js_scripts[src] = None

css_files = OrderedDict()


def add_css_file(src):
    css_files[src] = None

css_scripts = OrderedDict()


def add_css(src):
    css_scripts[src] = None


def print_head(title):
    print('Content-Type: text/html')
    print()

    print('''<!DOCTYPE html>
<html>
 <head>
  <meta charset="UTF-8">  
  <link rel="stylesheet" type="text/css" href="/css/jquery.datetimepicker.min.css"/ >
  <link rel="stylesheet" type="text/css" href="/css/html_base.css"/ >''')
    for src in css_files:
        print('''  <link rel="stylesheet" type="text/css" href="{}"/ >'''.format(src))
    for src in css_scripts:
        print('''  <style>
   {}   
  </style>'''.format(src))
    print('''<title>{}</title>  
 </head>
 <body><a href="/"><img src="/icons/logo.svg" width="200"/></a>'''.format(title))


def print_end():
    print(''' </body>
 <script type="application/javascript" src="/js/jquery-3.3.1.min.js"></script>
 <script type="application/javascript" src="/js/stend-script_v1.js"></script>''')
    for src in js_files.keys():
        print(' <script type="application/javascript" src="{}"></script>'.format(src))

    print('<script type="application/javascript">')
    for scr in js_scripts:
        print(scr)
    print('</script>')
    print('</html>')


def print_period():
    add_script_file('/js/jquery.datetimepicker.full.min.js')
    add_script_file('/js/stend_time.js')
    print('<fieldset><legend>Период</legend>')
    print('С <input name="from" id="datetimepicker_from" type="text" > до ')
    print('<input name="to" id="datetimepicker_to" type="text" >')
    print('</fieldset>')


ALL = 0
STEND_ONLY = 1


def print_stend_list(check_state=[], filter=STEND_ONLY):
    add_script_file('/js/stend_list.js')
    if filter == STEND_ONLY:
        condition = "WHERE stend_id<1000" 
    
    sql = '''SELECT `stend_id`,`description` FROM `stend_control_schema`.`stend_list` {};'''.format(condition)

    cnx = db.connect(**DB_CONFIG, database='stend_control_schema')
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(sql)

    stends = []
    stend_row = []
    for row in cursor:
        check = 'checked' if row['stend_id'] in check_state else ''
        stend_row.append('''
<td style="border-width: 1; border-style: solid; border-collapse: collapse">
<label title="{1}">
<input type="checkbox" name="st" value="{0}"  onclick="stendUserChecked(this);" {2}> {0}
</label>
</td>
'''.format(row['stend_id'], row['description'], check))
        if len(stend_row) == 10:
            stends.append('<tr>{}</tr>'.format('\n'.join(stend_row)))
            stend_row = []

    groups = []
    cursor.execute('SELECT `id`,`name` FROM `stend_control_schema`.`stend_groups`;')
    for row in cursor:
        groups.append('''<tr><td style="border-width: 1; border-style: solid; border-collapse: collapse">
<label><input class="stend-group-check" type="checkbox" value="{}" onclick="groupUserChecked(this);">{}</label>
</td></tr>'''.format(row['id'], row['name']))

    print('''<fieldset>
<legend>Стенды</legend>
<p>
<input type="button" value="выбрать все" onclick="stendCheckAll('st', true)"></input>
<input type="button" value="сбросить все" onclick="stendCheckAll('st', false)"></input>
</p>
<div style="display:inline-block;">
<table class="stend_table">
{}
</table>
</div>
<div style="display:inline-block; overflow: auto;">
<table class="stend_group_table">
{}
</table>
</div>
</fieldset>
'''.format('\n'.join(stends), '\n'.join(groups))
    )

    cursor = cnx.cursor(dictionary=False)
    cursor.execute('SELECT `stend`,`group` FROM `stend_control_schema`.`stend_group_bind`;')
    stend_group_bind = 'var stend_group_binds = [{}];'.format(','.join(['[{},{}]'.format(st, gr) for st, gr in cursor]))
    add_script(stend_group_bind)


def print_mod_list(check_state = []):    
    add_script_file('/js/stend_list.js')
    
    sql = '''SELECT name,description FROM stend_control_schema.modification_list ORDER BY name;'''

    cnx = db.connect(**DB_CONFIG, database='stend_control_schema')
    cursor = cnx.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()

    print('''
<fieldset><legend>Модификации</legend>
<input type="button" value="выбрать все" onclick="stendCheckAll('mod', true)"></input>
<input type="button" value="сбросить все" onclick="stendCheckAll('mod', false)"></input>
<table class="stend_table"><tr>''')
    n = 0
    for r in rows:
        n = n + 1
        check = 'checked' if r[0] in check_state else ''
        print('''<td style="border-width: 1; border-style: solid; border-collapse: collapse"><label title="{1}"><input type="checkbox" name="mod" value="{0}" {2}> {0}</label></td>'''.format(r[0], r[1], check))
        if n% 10 == 0:
            print('</tr><tr>')

    print('</tr></table></fieldset>')


if __name__ == "__main__":
    print('/n-------  {}  --------/n'.format(print_stend_list))
    print_stend_list()
    input()
        