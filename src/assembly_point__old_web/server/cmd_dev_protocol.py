import mysql.connector as db
import datetime
import codecs
import re
import xlsxwriter

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

def dev_protocol(task, dt_start=None, dt_end=None, stends=None):
    cond = ''
        
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

    cond += " and errors=0"

    task.setProgress(0.03)

    cnx = db.connect(**DB_CONFIG, database='work')
    cursor = cnx.cursor()
    sql = "SELECT COUNT(*) FROM (SELECT mac FROM test_descr WHERE id>0 {} GROUP BY mac) as tbl;".format(cond)
    cursor.execute(sql)
    record_count = cursor.fetchall()[0][0]

    task.setProgress(0.1)
    
    sql = "SELECT id,mac,stend_id,start,string FROM test_descr,full_report WHERE test_descr.id=full_report.test_id AND id IN (SELECT MAX(id) FROM work.test_descr WHERE id>0 {} GROUP BY mac);".format(cond)
    
    header_list = ["ID", "STEND", "DATE", "ADDRESS", "MODULE", "BATTERY"]
    cursor.execute(sql)

    task.setProgress(0.3)

    fname = task.createFile("report.xlsx")
    workbook = xlsxwriter.Workbook(fname)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})

    cols_width = [9.6, 7.5, 18, 10.5, 10, 10]

    for i in range(len(header_list)):
        worksheet.set_column(i, i, cols_width[i])
        worksheet.write(0, i, header_list[i], bold)
    
    result_rows = []
    readed=0
    
    row = cursor.fetchone()
    while row:
        task.checkBreak()
        mm='#ERR'
        res = re.findall('Модификация: (MM\d\d\d)', row[4])
        for v in res: mm = v

        res = re.findall('Измерение тока батареи: ([01]\.\d+).+OK', row[4])
        res1 = re.findall('OK +Ток батареи: ([01]\.\d+)', row[4])
                    
        bat = '#ERR'
        for bt in res:
            if float(bt) > 0.01: bat = float(bt)
        for bt in res1:
            if float(bt) > 0.01: bat = float(bt)

        r=(row[0], row[2], str(row[3]), row[1], mm, bat)

        result_rows.append(r)
        for i in range(len(r)):
            worksheet.write(readed+1, i, r[i])

        readed = readed + 1
        progress = readed / record_count
        task.setProgress(0.3 + 0.7*progress)

        row = cursor.fetchone()
        
    workbook.close()                    
    return {'header': header_list, 'rows': result_rows}

if __name__ == "__main__":
    while True:
        mac = input("Enter MAC address> ")
        data = report_condition(EmptyTask(), mac)
        print(data)        

    input("\npress enter to exit")