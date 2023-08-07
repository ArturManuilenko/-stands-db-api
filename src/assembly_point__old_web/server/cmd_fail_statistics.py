import mysql.connector as db
import datetime
import codecs
import re

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

def fail_statistics(task, stend_list, dt_from, dt_to):

    now = datetime.datetime.now()
    time_default={'d':now.day,'m':now.month,'y':now.year,'H':0,'M':0,'S':0}
    start = read_time(dt_from, time_default)

    now = datetime.datetime.now()
    time_default={'d':now.day,'m':now.month,'y':now.year,'H':now.hour,'M':now.minute,'S':now.second}
    end = read_time(dt_to, time_default)
    
    print("reading statistics for stends {} from {} to {}".\
              format(','.join([str(v) for v in stend_list]), start.strftime("%d.%m.%Y %H:%M:%S"), end.strftime("%d.%m.%Y %H:%M:%S")))
 
    cnx = db.connect(**DB_CONFIG, database='work')
    cursor = cnx.cursor()
    sql_begin = "SELECT id,serial,mac,stend_id,start,end,errors FROM work.test_descr WHERE "
    sql_stends = " or ".join(["stend_id={}".format(n) for n in stend_list])
    sql_date = "start > '{}' and start < '{}'".format(start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S"));

    sql = "SELECT COUNT(*) FROM work.test_descr WHERE errors>0 AND ({}) AND ({});".format(sql_stends, sql_date)
    cursor.execute(sql)
    record_count = cursor.fetchall()[0][0]

    sql = "SELECT * FROM work.test_descr,work.full_report WHERE test_descr.id=full_report.test_id"\
        " AND errors>0 AND ({}) AND ({});".format(sql_stends, sql_date)
    cursor.execute(sql)

    readed=0
    old_pers = 0

    row = cursor.fetchone()

    error_types = {}
    readed=0
    while row:
        task.checkBreak()
        
        id, serial, mac, stend_id, start, end, errors, test_id, descr = row

        res = re.findall('FAIL +(\d+ - .+)\n', descr)
        for err in res:
            if 'Окончание проверки' not in err:
                check_list = error_types.get(err, [])
                check_list.append( (mac,test_id,descr) )
                error_types[err] = check_list

        res = re.findall('Проверка завершена аварийно', descr)
        for err in res:
            check_list = error_types.get(err, [])
            check_list.append( (mac,test_id,descr) )
            error_types['Проверка завершена аварийно'] = check_list

        readed = readed + 1
        progress = readed / record_count
        task.setProgress(progress)
        row = cursor.fetchone()

    result_rows = []
    for err, descr in error_types.items():    
        result_rows.append( [len(descr), err, [v[1] for v in descr]] )
            
    return {'header': ["COUNT", "ERROR", "LIST"], 'rows': result_rows}

if __name__ == "__main__":
    stend_list = []
    list_str = input("enter stend list (example: '37-39,42', default 37-45)\n>")
    if len(list_str) == 0:
        list_str = "37-45"
        
    for el in list_str.split(","):
        vals = [int(v) for v in el.split("-")]
        if len(vals) == 1:
            stend_list.append(vals[0])
        else:
            stend_list.extend(range(vals[0], vals[1]+1))

    dt_from = input("enter start time (example: '01.01.2017 00:00' or '01.01 12:30' etc, default today 00:00)\n>")
    dt_to = input("enter end time (example: 01.01.2017 00:00 or 01.01 12:30 etc, default now)\n>")

    data = fail_statistics(EmptyTask(), stend_list, dt_from, dt_to)

    print('')
    print('{:>9} -> {}'.format("COUNT", "ERROR"))
    for row in data['rows']:
        print('{:9} -> {}'.format(row[0], row[1]))

    input("\npress enter to exit")