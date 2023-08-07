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

def read_time(time_str, time_default):
    time = ''
    date = ''
    vals = time_str.split(' ')
    if len(vals) == 2:
        date, time = vals
    elif ':' in vals[0]: time = vals[0]
    else: date = vals[0]
    
    keys = ['d','m','y']
    date = date.split('.') if len(date) else []
    for i in range(len(date)):
        time_default[keys[i]]=int(date[i])

    keys = ['H','M','S']
    time = time.split(':') if len(time) else []
    for i in range(len(time)):
        time_default[keys[i]]=int(time[i])

    return datetime.datetime(year=time_default['y'], month=time_default['m'], day=time_default['d'], 
                             hour=time_default['H'], minute=time_default['M'], second=time_default['S'])

def stend_versions_log(task, stend_list = [], type_list = [], full=True, dt_from=None, dt_to=None):
    cond = []
    if len(stend_list):
        cond.append('(' + ' or '.join(['stend={}'.format(stend) for stend in stend_list]) +')')
    if len(type_list):
        cond.append('(' + ' or '.join(["type='{}'".format(type) for type in type_list]) +')')

    now = datetime.datetime.now()
    time_default={'d':now.day,'m':now.month,'y':now.year,'H':0,'M':0,'S':0}
    if dt_from:        
        start = read_time(dt_from, time_default)
        cond.append("time > '{}'".format(start.strftime("%Y-%m-%d %H:%M:%S")))
    if dt_to:
        end = read_time(dt_to, time_default)
        cond.append("time <= '{}'".format(end.strftime("%Y-%m-%d %H:%M:%S")))
    headers = [
        'Стенд',
        'Файл стенда',
        'Тип',        
        'MD5',
        'Время',
        'Версия',
        'Ссылка',
        'Описание',
        ]
    cnx = db.connect(**DB_CONFIG, database='work')
    cursor = cnx.cursor()
    if full:
        sql = "SELECT COUNT(id) "\
            " FROM log_update WHERE {};".format(' AND '.join(cond))

        cursor.execute(sql)
        rows = cursor.fetchall()
        record_count = rows[0][0]

        sql = "SELECT stend,name,type,md5,time,version,source,descr "\
            " FROM log_update WHERE {};".format(' AND '.join(cond))
    else:
        sql = "SELECT COUNT(id) "\
            " FROM log_update WHERE id IN (SELECT MAX(id) FROM log_update WHERE {} GROUP BY stend, type);".format(' AND '.join(cond))

        cursor.execute(sql)
        rows = cursor.fetchall()
        record_count = rows[0][0]

        sql = "SELECT stend,name,type,md5,time,version,source,descr "\
           " FROM log_update WHERE id IN (SELECT MAX(id) FROM log_update WHERE {} GROUP BY stend, type) ORDER BY stend;".format(' AND '.join(cond))

    cursor.execute(sql)
    data = []

    readed = 0
    row = cursor.fetchone()
    while row:
        task.checkBreak()

        l = [str(v) for v in row]
        data.append(l)
        
        readed = readed + 1
        progress = readed / record_count
        task.setProgress(progress)
        row = cursor.fetchone()

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