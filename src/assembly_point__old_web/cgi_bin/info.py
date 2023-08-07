#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cgi
import cgitb
import html_nero

cgitb.enable()

form = cgi.FieldStorage()

html = html_nero.HtmlBase("Справочник", 'info.info')
html.print()
