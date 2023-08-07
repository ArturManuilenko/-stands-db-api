#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import cgi
import cgitb

import html_nero
import db
import random

cgitb.enable()

form = cgi.FieldStorage()
card_id = form.getvalue('login')
login = form.getvalue('login', '')
redirect_url = form.getvalue('redirect', os.environ.get("HTTP_REFERER"))
message = form.getvalue('message', None)
valid = False

if 'exit' in form:
    db.set_token(form.getvalue('exit', ''), '')
    html_nero.HtmlBase.redirect(redirect_url)

elif 'login' in form and 'password' in form:
    uinfo = db.get_web_user_info(login)
    if uinfo:
        user_login, passhash = uinfo
        if passhash == form.getvalue('password'):
            random.seed()
            token = login + '--' + hex(random.getrandbits(256))[2:]
            db.set_token(user_login, token)
            print("Set-cookie: user_token={}; path=/cgi_bin/; httponly".format(token))

            message = 'Вы успешно авторизировались на портале'
            valid = True
            if form.getvalue('redirect'):
                html_nero.HtmlBase.redirect(form.getvalue('redirect'))
        else:
            message = 'Указан неверный пароль'
    else:
        message = 'Пользователь с указанным логином или e-mail не найден'

html_nero.print_header('Страница авторизации')


html = html_nero.HtmlBase()
s='''
    <form action="login.py" method="post">
    Имя пользователя или e-mail: <br>
    <input type="text" name="login" value="{}"><Br>
    Пароль: <br>
    <input type="password" name="password" value=""><Br>
    <input type="hidden" name="redirect" value="{}"><Br>
    <p><input type="submit" ></p>
    </form>
'''.format(login, redirect_url)

if message:
    html.add('<p>{}<p>'.format(message))
    #print('<p>{}<p>'.format(message))
if not valid:
    html.add(s)
    #print(s)

#nero_stend.print_footer()
html.print()
