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

def report_condition(task, mac=None, dt_start=None, dt_end=None, stends=None, report=True, serial=None):
    cond = ''
    if mac is not None:
        cond += ' and test_descr.mac={}'.format(mac)

    if serial is not None:
        cond += " and test_descr.serial='{}'".format(serial)
        
    if stends:
        cond += ' and (' + ' or '.join(['stend_id={}'.format(n) for n in stends]) + ')'

    if dt_start:
        now = datetime.datetime.now()
        time_default={'d':now.day,'m':now.month,'y':now.year,'H':0,'M':0,'S':0}
        start = read_time(dt_start, time_default)
        cond += """ and start>'{}'""".format(start.strftime("%Y-%m-%d %H:%M:%S"))

    if dt_end:
        now = datetime.datetime.now()
        time_default={'d':now.day,'m':now.month,'y':now.year,'H':now.hour,'M':now.minute,'S':now.second}
        end = read_time(dt_end, time_default)
        cond += """ and start<'{}'""".format(end.strftime("%Y-%m-%d %H:%M:%S"))


    cnx= db.connect(**DB_CONFIG, database='work')
    cursor = cnx.cursor()
    sql = "SELECT COUNT(id) FROM test_descr WHERE id>0 {};".format(cond)
    cursor.execute(sql)
    record_count = cursor.fetchall()[0][0]

    if report:
        sql = "SELECT test_descr.id,serial,mac,stend_id,start,end,errors,string FROM test_descr,full_report WHERE test_descr.id=full_report.test_id {};".format(cond)
        header_list = ["ID", "SERIAL", "MAC", "STEND", "START", "END", "ERRORS", "REPORT"]
    else:
        sql = "SELECT id,serial,mac,stend_id,start,end,errors FROM test_descr WHERE id>0 {};".format(cond)
        header_list = ["ID", "SERIAL", "MAC", "STEND", "START", "END", "ERRORS"]
    cursor.execute(sql)

    
    result_rows = []
    readed=0
    
    row = cursor.fetchone()
    while row:
        task.checkBreak()
        r=list(row)
        r[4] = str(r[4])
        r[5] = str(r[5])
        result_rows.append(r)

        readed = readed + 1
        progress = readed / record_count
        task.setProgress(progress)

        row = cursor.fetchone()
                    
    return {'header': header_list, 'rows': result_rows}

if __name__ == "__main__":
    while True:
        mac = input("Enter MAC address> ")
        data = report_condition(EmptyTask(), mac)
        print(data)        

    input("\npress enter to exit")