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

def version_statistics(task, stend_list, dt_from, dt_to, syccess_only = False, group_id = False):

    now = datetime.datetime.now()
    time_default={'d':now.day,'m':now.month,'y':now.year,'H':0,'M':0,'S':0}
    start = read_time(dt_from, time_default)

    now = datetime.datetime.now()
    time_default = {'d': now.day, 'm': now.month, 'y': now.year, 'H': now.hour, 'M': now.minute, 'S': now.second}
    end = read_time(dt_to, time_default)
     
    cnx = db.connect(**DB_CONFIG, database='work')
    cursor = cnx.cursor()

    sql_stends = " or ".join(["stend_id={}".format(n) for n in stend_list])
    sql_date = "start > '{}' and start < '{}'".format(start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S"));

    cond = "({}) and ({})".format(sql_stends, sql_date)

    if syccess_only:
        cond += " AND errors=0"

    sql = "SELECT COUNT(*) FROM test_descr WHERE {};".format(cond)
    cursor.execute(sql)
    rows = cursor.fetchall()

    record_count = rows[0][0]


    sql = "SELECT string FROM work.test_descr,work.full_report WHERE test_descr.id=full_report.test_id AND {};".format(cond)
    cursor.execute(sql)

    stat={}

    readed=0

    reg = re.compile('Прошивка версии ((\d+)\.\d+\.\d+\.\d+)');

    row = cursor.fetchone()
    while row:
        task.checkBreak()        
        res = reg.findall(row[0])
        if len(res) == 0:
            stat["без версии"] = stat.get("без версии", 0) + 1
        else:
            if group_id:
                stat[res[0][1]+'.x.x.x'] = stat.get(res[0][1]+'.x.x.x', 0) + 1
            else:
                stat[res[0][0]] = stat.get(res[0][0], 0) + 1

        readed = readed + 1
            
        progress = readed / record_count
        task.setProgress(progress)

        row = cursor.fetchone()
        
    result_rows = []

    all_count = 0
    for ver, count in stat.items():
        result_rows.append( [ver, count] )
        all_count += count

    result_rows.sort()
    result_footer = []
    result_footer.append( ['ALL', all_count] )
    
    return {'header': ("VERSION", "COUNT"), 'rows': result_rows, 'footer': result_footer}

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

    data = check_statistics(EmptyTask(), stend_list, dt_from, dt_to)

    
    print("{:>9}{:>9}{:>9}{:>9}{:>9}{:>9}".format("STEND", "MOD", "COUNT", "OK", "FAIL", "REPEATE", "FAIL&OK"))
    for r in data['rows']:
        print("{:>9}{:>9}{:>9}{:>9}{:>9}{:>9}".format(*r))


    print('---------'*6)
    for r in data['footer']:        
        print("{:>9}{:>9}{:>9}{:>9}{:>9}{:>9}".format(*r))

    input("\npress enter to exit")