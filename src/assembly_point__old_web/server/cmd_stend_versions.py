import mysql.connector as db
import datetime
import codecs

from src.assembly_point__old_web.env import DB_CONFIG


class EmptyTask:
    def __init__(self):
        self.progress = 0.0
        self.data = {}
    def checkBreak(self):
        return False
    def setProgress(self, value):
        self.progress = 1.0 if value > 1.0 else value
    def open(self, file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
        return open(file, mode, buffering, encoding, errors, newline, closefd, opener) 

def stend_versions(task, stend_list = [], type_list = []):
    cond = ''
    if len(stend_list):
        cond += ' and (' + ' or '.join(['stend={}'.format(stend) for stend in stend_list]) +')'
    if len(type_list):
        cond += ' and (' + ' or '.join(["type='{}'".format(type) for type in type_list]) +')'

    headers = [
        'Стенд',
        'Файл стенда',
        'ID',
        'Имя',
        'Тип',
        'MD5',
        'CRC',
        'Время',
        'Версия',
        'Ссылка',
        'Описание',
        ]

    
    cnx = db.connect(**DB_CONFIG, database='stend_control_schema')
    cursor = cnx.cursor()
    sql = "SELECT stend,stend_update.name,firm_files.id,firm_files.name,type,md5,crc32,time,version,repository,comment "\
    " FROM stend_update,firm_files WHERE stend_update.file=firm_files.id {};".format(cond)
    cursor.execute(sql)
    rows = cursor.fetchall()
    data = []
    for r in rows:
        l = list(r)
        l[7] = str(l[7])
        data.append(l)
    strs = [r[0] for r in rows]
    return  {'header': headers, 'rows': data}

if __name__ == "__main__":
    stend_list = []
    list_str = input("enter stend list (example: '37-39,42', default ALL)\n>")
    if len(list_str) > 0:        
        for el in list_str.split(","):
            vals = [int(v) for v in el.split("-")]
            if len(vals) == 1:
                stend_list.append(vals[0])
            else:
                stend_list.extend(range(vals[0], vals[1]+1))

    type_str = input("enter type list (example: BDS, default ALL)\n>")
    type_list = list(type_str)
    
    data = stend_versions(EmptyTask(), stend_list, type_list)
    
    for r in data['rows']:
        for i in range(len(r)):
            print('{}: {}'.format(data['header'][i], r[i]))

        print('')

    input("\npress enter to exit")