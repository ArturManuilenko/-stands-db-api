import mysql.connector as db
import datetime
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

def check_statistics(task, stend_list, dt_from, dt_to, group_by_mod = False):

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

    sql = "SELECT COUNT(*) FROM work.test_descr WHERE ({}) and ({});".format(sql_stends, sql_date)
    cursor.execute(sql)
    rows = cursor.fetchall()

    record_count = rows[0][0]
    
    print("found {} records\n".format(record_count))

    if group_by_mod:
        sql = "SELECT mac,errors,stend_id,serial,string FROM test_descr,full_report WHERE test_descr.id=full_report.test_id and ({}) and ({});".format(sql_stends, sql_date)
    else:
        sql = "SELECT mac,errors,stend_id,serial FROM work.test_descr WHERE ({}) and ({});".format(sql_stends, sql_date)
    cursor.execute(sql)

    common = {}
    stat={}
    for stend in stend_list:
        stat[stend]={}

    readed=0
    old_progress = 0.0

    row = cursor.fetchone()
    while row:
        task.checkBreak()
        mac, errors, stend, serial = row[:4]
        if mac == 0:
            try:
                mac = int(serial,16) << 32
            except:
                pass
        modification = ''
        if group_by_mod:
            res = re.findall('Модификация: (MM\d\d\d)', row[4])
            if len(res) > 0:
                modification = res[0]
            else:
                modification = '-'
            
        info = stat[stend].get(modification, {'ok':set(), 'fail':set(), 'repok':set(), 'rep':0, 'n':0, 'noid':0})
        stat[stend][modification] = info

        common_stat = common.get(modification, {'ok':set(), 'fail':set(), 'repok':set(), 'rep':0, 'n':0, 'noid':0})
        common[modification] = common_stat

        if (mac in info['ok']) or (mac in info['fail']):
            info['rep'] = info['rep'] + 1
        info['n'] = info['n'] + 1

        if (mac in common_stat['ok']) or (mac in common_stat['fail']):
            common_stat['rep'] = common_stat['rep'] + 1
        common_stat['n'] = common_stat['n'] + 1

        if mac == 0:
            info['noid'] += 1
            common_stat['noid'] += 1

        if errors == 0:
            info['ok'].add(mac)
            if mac in info['fail']:
                info['repok'].add(mac)
                info['fail'].remove(mac)

            common_stat['ok'].add(mac)
            if mac in common_stat['fail']:
                common_stat['repok'].add(mac)
                common_stat['fail'].remove(mac)
        else:
            if mac in info['ok']:
                info['repok'].add(mac)

                common_stat['repok'].add(mac)
            else:
                info['fail'].add(mac)

                common_stat['fail'].add(mac)

        readed = readed + 1
            
        progress = readed / record_count
        task.setProgress(progress)

        if progress != old_progress:
            print("{}%".format(int(progress*100)), end='\r')
            old_progress = progress

        row = cursor.fetchone()
        
    result_rows = []

    n = ok = fail = rep = repok = noid = 0
    for stend, info_mod in stat.items():
        if len(info_mod) == 0: info_mod={'': {'ok':set(), 'fail':set(), 'repok':set(), 'rep':0, 'n':0, 'noid':0}}
        for mod,info in info_mod.items():
            sum = len(info['ok']) + len(info['fail'])
            pers =  '{:.2f}%'.format(100.0 * len(info['fail']) / sum) if sum else '-'

            result_rows.append( [stend, mod, info['n'], len(info['ok']), len(info['fail']), info['rep'], len(info['repok']), pers, info['noid']] )

            n += info['n']
            ok += len(info['ok'])
            fail += len(info['fail'])
            rep += info['rep']
            repok += len(info['repok'])
            noid += info['noid']

    result_footer = []
    sum = ok + fail
    pers =  '{:.2f}%'.format(100.0 * fail / sum) if sum else '-'
    result_footer.append( ['ALL', '', n, ok, fail, rep, repok, pers, noid] )

    n = ok = fail = rep = repok = noid = 0
    for mod,info in common.items():
        sum = len(info['ok']) + len(info['fail'])
        pers =  '{:.2f}%'.format(100.0 * len(info['fail']) / sum) if sum else '-'

        result_footer.append( ['COMMON', mod, info['n'], len(info['ok']), len(info['fail']), info['rep'], len(info['repok']), pers, info['noid']] )

        n += info['n']
        ok += len(info['ok'])
        fail += len(info['fail'])
        rep += info['rep']
        repok += len(info['repok'])
        noid += info['noid']

    if group_by_mod: 
        sum = ok + fail
        pers =  '{:.2f}%'.format(100.0 * fail / sum) if sum else '-'
        result_footer.append( ['COMMON', '', n, ok, fail, rep, repok, pers, noid] )

    return {'header': ("STEND", "MOD", "COUNT", "OK", "FAIL", "REPEATE", "FAIL&OK", "FAIL %", "NOID"), 'rows': result_rows, 'footer': result_footer}

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

    
    print("{:>9}{:>9}{:>9}{:>9}{:>9}{:>9}{:>9}{:>9}{:>9}".format(*data['header']))
    for r in data['rows']:
        print("{:>9}{:>9}{:>9}{:>9}{:>9}{:>9}{:>9}{:>9}{:>9}".format(*r))


    print('---------'*9)
    for r in data['footer']:        
        print("{:>9}{:>9}{:>9}{:>9}{:>9}{:>9}{:>9}{:>9}{:>9}".format(*r))

    input("\npress enter to exit")