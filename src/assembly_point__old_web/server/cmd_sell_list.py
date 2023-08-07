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

def sell_list(task, dt_start=None, dt_end=None, stends=None, just_good=True, mods=None):
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

    if just_good:
        cond += " and errors=0"

    task.setProgress(0.03)

    cnx = db.connect(**DB_CONFIG, database='work')
    cursor = cnx.cursor()
    sql = "SELECT COUNT(*) FROM (SELECT mac FROM test_descr WHERE id>0 {} GROUP BY mac) as tbl;".format(cond)
    cursor.execute(sql)
    record_count = cursor.fetchall()[0][0]

    task.setProgress(0.1)
    
    sql = "SELECT id,serial,mac,stend_id,start,end,errors,string FROM test_descr,full_report WHERE id=test_id AND id IN (SELECT MAX(id) FROM work.test_descr WHERE id>0 {} GROUP BY mac);".format(cond)
    header_list = ["ID", "SERIAL", "MAC", "STEND", "START", "END", "ERRORS", "MODIFICATION"]
    cursor.execute(sql)

    task.setProgress(0.3)

    fname = task.createFile("result.xlsx")
    workbook = xlsxwriter.Workbook(fname)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})

    cols_width = [8.9, 34.2, 12, 6, 17.6, 17.6, 7.2, 17.6]

    for i in range(len(header_list)):
        worksheet.set_column(i, i, cols_width[i])
        worksheet.write(0, i, header_list[i], bold)
    
    result_rows = []
    readed=0
    xls_row=0

    regexp = re.compile("Модификация: (.*)$")
    
    row = cursor.fetchone()
    while row:
        task.checkBreak()
        r=list(row)
        r[4] = str(r[4])
        r[5] = str(r[5])

        descr = r[7]

        re_res = regexp.findall(descr)
        r[7] = re_res[0] if len(re_res) else '---'

        if len(mods) == 0 or r[7] in mods:
            result_rows.append(r)  
            
            xls_row += 1
            for i in range(len(r)):
                worksheet.write(xls_row, i, r[i])
            

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