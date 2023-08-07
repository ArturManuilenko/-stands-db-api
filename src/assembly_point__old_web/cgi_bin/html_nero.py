import codecs
import sys
import os
import http.cookies
import urllib
from typing import Optional

import db

import html_blocks
from html_config import MAIN_MENU_ITEMS, SUB_MENU_ITEMS

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
user_token = cookie.get("user_token")
#получить куки

header_start_format = '''
<!DOCTYPE html>
<html>
 <head>
  <meta charset="utf-8">
  <title>Система управления тестовыми стендами NERO ELECTRONICS - {title}</title>
  <link href="/css/cssmain.css" rel="stylesheet">
{css}

{js}
 </head>
 <body>
{menu}
  <div class="main">
'''

menu_format = '''
  <div class="header">
    <div class="main_menu">
       <table width="100%">
        <tr>
         <td width="100px">
            <a href="/cgi_bin/index.py" class="float: left;">
            <img src="/icons/stend.jpg" height="90px" align="left">
            </a>
         </td>
         <td>
            <div style="height: 35px">
                <a href="/cgi_bin/index.py" style="float: left;"><img src="/icons/logo.svg" height="35px"></a>
                <div class="login">
                {login_data}
                </div>
            </div>
            <div class="mainmenu">{mainmenu}</div>
            <div class="submenu">{submenu} <div class="rsubmenu">{rsubmenu}</div></div>
         </td>
        </tr>
       </table>
    </div>
  </div>
'''
#<div class="menuline"/>
o = '''
    <div class="menu_group">

    </div>
    <div class="menu_group">
     <div class="menu_row" height="35%">
      <div class="menu_item" align="left"><img src="/icons/logo.svg" style="height:100%"></div>
      <div class="menu_item" align="right"></div>
     </div>
     <div class="menu_row" height="35%">{menu}</div>
     <div class="menu_row" height="30%">{submenu}</div>
    </div>

'''
footer_data = '''
  </div>
  <div class="footer">
© 2020 ООО «Неро Электроникс»
  </div>
'''


def urlQuote(url):
    return urllib.parse.quote(url)


class HtmlBase:
    def redirect(url):
        print('''Content-Type: text/html; charset=UTF-8
Location: {0}

<html>
<head>
<meta http-equiv="refresh" content="0;url={0}" />
<title>Вы будете перенаправлены на другую страницу</title>
</head>
<body>
Перенаправление... <a href="{0}">Нажмите на ссылку если не было выполнено автоматическое перенаправление</a>
</body>
</html>
'''.format(url))
        exit()

    def __init__(self, title: Optional[str] = '', page: Optional[str] = 'main.', submenu: Optional = None) -> None:
        self.access_info = db.access(user_token.value if user_token else '')
        self.http_headers = ['Content-Type: text/html; charset=UTF-8']
        self.title = title
        self.css_files = [f'/css/cssmain.css']
        self.css = []
        self.js_files = [f'/js/jquery-3.3.1.min.js']
        self.items = []
        self.scripts = []

        self.page, self.sub_page = page.split('.')
        self.submenu = submenu

    def menu_str(self):
        if self.access_info['login']:
            login_data = f'''  <a href="/cgi_bin/login.py?exit={urllib.parse.quote(self.access_info['login'])}" class="menu_button">
   <img src="icons/logout.png" height=32> Выйти
  </a>'''
        else:
            login_data = f'''  <a href="/cgi_bin/login.py" class="menu_button">
   <img src="/icons/login.png" height=32> Войти
  </a>'''

        menu = ['''<a href="{}"{} width="{}%"><div style="height:100%; padding: 5px;">{}</div></a>'''.format(
            url,
            ' class="msel"' if self.page == name else '',
            100 / len(MAIN_MENU_ITEMS),
            text
            ) for text, name, url in MAIN_MENU_ITEMS]

        current_sub_menu_items = SUB_MENU_ITEMS[self.page]
        submenu = ['''<a href="{}"{} width="{}%">{}</a>'''.format(
            url,
            ' class="msel"' if self.sub_page == name else '',
            100 / len(current_sub_menu_items),
            text
            ) for text, name, url in current_sub_menu_items]

        rsubmenu = []
        if self.submenu:
            rsubmenu.append('<span>{}</span>'.format(self.submenu))

        return menu_format.format(login_data=login_data,
                                  mainmenu='\n'.join(menu),
                                  submenu='\n'.join(submenu),
                                  rsubmenu='\n'.join(rsubmenu)
                                  )

    def print(self):
        print('\n'.join(self.http_headers))




        print(header_start_format.format(
            title=self.title,
            #css = '  <style type="text/css">\n{}\n  </style>'.format('\n'.join(self.css)) if len(self.css) else '',
            css='\n'.join(['   <link href="{}" rel="stylesheet" type="text/css" />'.format(f) for f in self.css_files]),
            js='\n'.join(['  <script type="application/javascript" src="{}"></script>'.format(f) for f in self.js_files]),
            menu=self.menu_str()
            ))

        for item in self.items:
            print(str(item))

        print(footer_data)
        if len(self.scripts):
            print('  <script type="application/javascript" >\n{}\n  </script>'.format('\n'.join(self.scripts)))
        print(' </body>\n</html>')

    def add(self, item):
        self.items.append(item)

    def add_block(self, tag, param: Optional[str] = '') -> html_blocks.Block:
        block = html_blocks.Block(tag, param)
        self.add(block)
        return block

    def add_js_files(self, *args) -> None:
        for filename in args:
            self.js_files.append(filename)

    def add_script(self, text) -> None:
        self.scripts.append(text)

    def add_css_files(self, *args):
        for filename in args:
            self.css_files.append(filename)


def print_header(page: Optional[str] = '', scripts=[], css=[]):
    access_info = db.access(user_token.value if user_token else '')

    if access_info['login']:
        logindata='<a href="/cgi_bin/login.py?exit={}" class="menu_button"><img src="/icons/logout.png" height=32> Выйти</a>'.format(urllib.parse.quote(access_info['login']))
    else:
        logindata='<a href="/cgi_bin/login.py" class="menu_button"><img src="/icons/login.png" height=32> Войти</a>'



    jsdata = '<script type="application/javascript" >\n{}\n</script>'.format('\n'.join(scripts)) if scripts else ''
    cssdata = ' <style type="text/css">\n{}\n</style>'.format('\n'.join(css)) if css else ''

    print('''Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Система управления доступом NERO ELECTRONICS - {page}</title>
        <link href="/css/cssmain.css" rel="stylesheet">
        {cssdata}
    </head>
<body>
<script type="application/javascript" src="/js/jquery-3.3.1.min.js"></script>
{jsdata}
<div class="header">
    <div class="main_menu">
        <a href="/">
        <img src="/icons/turniket.png" height="100%">
        <img src="/icons/logo.svg" height="50%">
        </a>

        <span>
        {logindata}
        </span>
    </div>
</div>
<div class="body">
<p>
'''.format(page=page, cssdata=cssdata, jsdata=jsdata, logindata=logindata))

def print_footer(scripts = None):
    jsdata = '<script type="application/javascript" >\n{}\n</script>'.format('\n'.join(scripts)) if scripts else ''
    print('''
</div>
<div class="footer">
© 2020 ООО «Неро Электроникс»
</div>
{}
</body>
</html>'''.format(jsdata))

def check_access(admin = False):
    if admin:
        if user_token:

            res = db.access(user_token.value)
            if res['login']:
                return res
            else:
                HtmlBase.redirect('login.py')
        else:
            HtmlBase.redirect('login.py')
