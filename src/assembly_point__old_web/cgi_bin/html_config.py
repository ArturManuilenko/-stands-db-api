#!/usr/bin/env python3
# -*- coding: utf-8 -*-

MAIN_MENU_ITEMS = [
    ('Главная', 'main', '/cgi_bin/index.py'),
    ('Статистика', 'state', '/cgi_bin/statistics.py'),
    ('Отчеты', 'report', '/cgi_bin/calibrprotocol.py'),
    ('Стенды', 'stend', '/cgi_bin/stendlist.py'),
    ('Калибровка', 'calibration', '/cgi_bin/calibrlist.py'),
    ('Информация', 'info', '/cgi_bin/info.py'),
    ('Управление', 'control', '/cgi_bin/control.py'),
]

SUB_MENU_ITEMS = {
    'main': [],
    'state': [
        ('Общая', 'statistics', '/cgi_bin/statistics.py'),
        ('Перемещения', 'statemove', '/cgi_bin/statemove.py'),
       ],
    'report': [
        ('Поверка', 'calibrprotocol', '/cgi_bin/calibrprotocol.py'),
        ('Энергомера', 'energomerareport', '/cgi_bin/energomerareport.py'),
       ],
    'stend': [
        ('Список', 'stendlist', '/cgi_bin/stendlist.py'),
        ('Группы', 'stendgroups', '/cgi_bin/stendgroups.py'),
       ],
    'calibration': [
        ('Запуски', 'calibrlist', '/cgi_bin/calibrlist.py'),
        ('Приборы', 'calibrdevlist', '/cgi_bin/calibrdevlist.py'),
       ],
    'info': [
        ('Справочник', 'info', '/cgi_bin/info.py'),
        ('Модификации', 'modlist', '/cgi_bin/modlist.py'),
        ('Версии', 'versiondevs', '/cgi_bin/versiondevs.py'),
       ],
    'control': [
       ],
}
