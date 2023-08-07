#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cgi
import cgitb
import html_nero
import html_blocks

import mysql.connector as db
import mysql.connector.cursor
import time

from src.assembly_point__old_web.env import DB_CONFIG

cgitb.enable()

form = cgi.FieldStorage()
report_id = form.getvalue('id')

html = html_nero.HtmlBase("Лог калибровки/поверки прибора", 'calibration.calibrlog', 'Лог')

pre = html_blocks.Block('pre')
if report_id is not None:
    connection = db.connect(**DB_CONFIG, database='calibration')
    cursor = connection.cursor(dictionary=True, buffered=True)
    cursor.execute("SELECT `log` FROM `stage_log` WHERE `report`=%s ORDER BY `number`;", (report_id,))
    for row in cursor:
        pre.add(row['log'])

bl = html_blocks.Block('div', ' ')
bl.add(pre)

html.add(bl)
html.print()
