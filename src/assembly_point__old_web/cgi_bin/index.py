#!/usr/bin/env python

import cgi
import cgitb

from src.assembly_point__old_web.cgi_bin import html_nero

cgitb.enable()

form = cgi.FieldStorage()

html = html_nero.HtmlBase("Тестовые стенды Nero Electronics", 'main.')

html.add('<br>')

html.add('''
     <p><a href="/cgi_bin/old/get_statistics.py">Статистика</a></p>
     <p><a href="/cgi_bin/old/get_fail_statistics.py">Статистика ошибок</a></p>
     <p><a href="/cgi_bin/old/get_version_statistics.py">Статистика версий</a></p>
     <p><a href="/cgi_bin/old/get_report_id.py">Полный отчет</a></p>
     <p><a href="/cgi_bin/old/get_report_mac.py">Отчеты по MAC адресу</a></p>
     <p><a href="/cgi_bin/old/get_report_serial.py">Отчеты по серийному номеру</a></p>
     <p><a href="/cgi_bin/old/get_stend_versions.py">Назначенные версии прошивок</a></p>
     <p><a href="/cgi_bin/old/get_stend_versions_log.py">Загруженные версии прошивок</a></p>
     <p><a href="/cgi_bin/old/get_stend_update_log.py">Лог обновлений</a></p>
     <p><a href="/cgi_bin/old/get_report_list.py">Список проверок</a></p>
     <p><a href="/cgi_bin/old/get_sell_list.py">Список на отгрузку</a></p>
     <p><a href="/cgi_bin/old/get_erased.py">Незапрограммированные</a></p>
     <p><a href="/cgi_bin/old/get_dev_protocol.py">Протокол разработки</a></p>''')


html.print()
