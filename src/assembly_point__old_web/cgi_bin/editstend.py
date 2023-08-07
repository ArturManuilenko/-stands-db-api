#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cgi
import cgitb
import html_nero
import html_blocks

import mysql.connector as db

from src.assembly_point__old_web.env import DB_CONFIG

cgitb.enable()

form = cgi.FieldStorage()

html = html_nero.HtmlBase("Подробно", 'stend.editstend', 'Подробно')
html.add_js_files('/js/value_editor.js')
html.add_css_files('/css/value_editor.css')


connection = db.connect(**DB_CONFIG, database='stend_control_schema')
cursor = connection.cursor(dictionary=True)

stend_id = form.getvalue('id', -1)
nav = form.getvalue('nav', '')

if stend_id == -1 and nav == '':
    nav = 'first'

if stend_id == -1:
    cursor.execute("SELECT MIN(stend_id) AS id FROM stend_list;")
    res = cursor.fetchone()
    if res:
        stend_id = res['id']

if nav == 'first':
    #навигация
    cursor.execute( "SELECT stend_id FROM stend_list ORDER BY stend_id limit 1;" )
    row = cursor.fetchone()
    if row:
        html_nero.HtmlBase.redirect('editstend.py?id={}'.format(row['stend_id']))
    else:
        html.add('''
        ОШИБКА: стенд не найден
        ''')

elif nav == 'last':
    #навигация
    cursor.execute( "SELECT stend_id FROM stend_list ORDER BY stend_id DESC limit 1;" )
    row = cursor.fetchone()
    if row:
        html_nero.HtmlBase.redirect('editstend.py?id={}'.format(row['stend_id']))
    else:
        html.add('''
        ОШИБКА: стенд не найден
        ''')
elif nav == 'next':
    #навигация
    cursor.execute("SELECT stend_id FROM stend_list "
                   "WHERE stend_id>%s "
                   "ORDER BY stend_id limit 1;", (stend_id,))
    row = cursor.fetchone()
    if row:
        html_nero.HtmlBase.redirect('editstend.py?id={}'.format(row['stend_id']))
    else:
        html.add('''
        ОШИБКА: стенд не найден
        ''')
elif nav == 'prev':
    #навигация
    cursor.execute("SELECT stend_id FROM stend_list "
                   "WHERE stend_id<%s "
                   "ORDER BY stend_id DESC limit 1;", (stend_id,))
    row = cursor.fetchone()
    if row:
        html_nero.HtmlBase.redirect('editstend.py?id={}'.format(row['stend_id']))
    else:
        html.add('''
        ОШИБКА: стенд не найден
        ''')
else:
    firm_file_names = {'param':'параметров стенда',
                     'platform':'настроек стенда',
                     'firm':'прошивки прибора',
                     'boot':'бутлоадера стенда',
                     'update':'прошивки стенда',
                     }
    #редактирование
    cursor.execute("SELECT stend_id,description,generate FROM stend_list WHERE stend_id=%s;", (stend_id,))

    res = cursor.fetchall()
    if len(res):
        data = res[0]

        cursor.execute('SELECT time,param,platform FROM stend_control_schema.stend_crc WHERE id=%s;', (stend_id,))
        crc = cursor.fetchall()
        crc = crc[0] if len(crc) else {'time':'', 'param':0, 'platform':0}

        updates = []
        cursor.execute('SELECT `stend_update`.`name` as "name",`file`,`enable`,`time`,`version`,`repository`,`comment`'
                    ' FROM `stend_control_schema`.`stend_update` JOIN `stend_control_schema`.`firm_files` '
                    'ON `stend_update`.`file` = `firm_files`.`id` '
                    'WHERE `stend`=%s',
                    (stend_id,)
                    )
        for r in cursor:
            updates.append({'name': firm_file_names.get(r['name'],r['name']), 'en': r['enable'], 'file':r['name']})


        config_crcs = []
        cursor.execute('SELECT `name`,`crc32`,`time` FROM `stend_control_schema`.`current_config_files` WHERE stend=%s;', (stend_id,))
        for r in cursor:
            config_crcs.append({'name': firm_file_names.get(r['name'],r['name']), 'file':r['name'],
                                'info': '{:08X} установлена {}' .format(r['crc32'] ,r['time'])})

        #db_server = 0
        stend_configs = {}
        cursor.execute('SELECT `name`, `value` FROM `stend_control_schema`.`stend_config` '
                       'JOIN `stend_control_schema`.`stend_config_ids` ON `stend_config_ids`.`id`=`stend_config`.`config` '
                       'WHERE `stend`=%s;',
                       (stend_id,)
                       )
        for row in cursor:
            stend_configs[row['name']] = row['value']

        navi = html_blocks.ItemNavigation('editstend.py', stend_id, data['description'])
        html.add(navi)

        form = html_blocks.EditForm()
        form.add_info('Номер', data['stend_id'])
        # param - Параметров  platform - настроек
        if html.access_info['admin']:

            cmd = '''{{cmd: 'modify_stend', id: {}}}'''.format(stend_id)
            form.add_text_edit('Описание', data['description'], 'descr', cmd)

            for file in updates:
                cmd = '''{{cmd: 'modify_stend_update_en', id: {}, file: '{}'}}'''.format(stend_id, file['file'])
                form.add_row('Обновление ' + file['name'], file['file'], cmd).add_combo_box('enabled',
                                                                                            ((0,'запрещено'),(1,'разрешено')), file['en'])

            for file in config_crcs:
                cmd = '''{{cmd: 'register_stend_config', id: {}, file: '{}'}}'''.format(stend_id, file['file'])
                form.add_row('Текущая контрольная сумма ' + file['name']).add_text(file['info']).add_button('Зарегистрировать', cmd)

            cmd = '''{{cmd: 'modify_stend', id: {}}}'''.format(stend_id)
            form.add_row('Контрольные суммы', 'crc', cmd).add_text('параметры:').add_text_edit('crc_param', '{:08X}'.format(crc['param']))\
                      .add_text(' настройки:').add_text_edit('crc_platform', '{:08X}'.format(crc['platform'])).add_text(crc['time'])

            cmd = '''{{cmd: 'modify_stend_config', id: {}}}'''.format(stend_id)
            form.add_row('Режим доступа к БД', 'db_server', cmd).add_combo_box('db_server',
                                                                               (('0','Прямой доступ'),('1','Сервер')),
                                                                               stend_configs.get('db_server',0))

            cmd = '''{{cmd: 'modify_stend_config', id: {}}}'''.format(stend_id)
            form.add_row('Повторная проверка', 'refirm_control', cmd).add_combo_box('refirm_control',
                                                                                    (('0','Запрещена для успешно проверенных'),('1','Разрешена')),
                                                                                    stend_configs.get('refirm_control',0))

            cmd = '''{{cmd: 'modify_stend_config', id: {}}}'''.format(stend_id)
            form.add_row('Действия при ошибках', 'break_mode', cmd).add_combo_box('break_mode',
                                                                                  (('0','Продолжать при некритических'),('1','Прервать проверку')),
                                                                                  stend_configs.get('break_mode',0))
        else:
            form.add_info('Выделение адресов', 'разрешено' if data['generate'] else 'запрещено')

            for file in updates:
                form.add_info('Обновление ' + file['name'], 'разрешено' if file['en'] else 'запрещено')

            for file in config_crcs:
                form.add_info('Текущая контрольная сумма ' + file['name'], file['info'])

            form.add_info('Контрольные суммы', 'Параметры: {:08X} Настройки:{:08X} {}'.format(crc['param'], crc['platform'], crc['time']))

        html.add(form)
    else:
        html.add('''
    ОШИБКА: стенд не найден
    ''')

html.print()
