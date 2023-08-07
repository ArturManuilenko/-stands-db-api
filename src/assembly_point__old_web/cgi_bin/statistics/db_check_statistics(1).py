import mysql.connector as db
import datetime
import codecs

from src.assembly_point__old_web.env import DB_CONFIG


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

        time_str = input("enter start time (example: '01.01.2017 00:00' or '01.01 12:30' etc, default today 00:00)\n>")
        now = datetime.datetime.now()
        time_default={'d':now.day,'m':now.month,'y':now.year,'H':0,'M':0,'S':0}
        start = read_time(time_str, time_default)

        time_str = input("enter end time (example: 01.01.2017 00:00 or 01.01 12:30 etc, default now)\n>")
        now = datetime.datetime.now()
        time_default={'d':now.day,'m':now.month,'y':now.year,'H':now.hour,'M':now.minute,'S':now.second}
        end = read_time(time_str, time_default)
        
        print("reading statistics for stends {} from {} to {}".\
              format(','.join([str(v) for v in stend_list]), start.strftime("%d.%m.%Y %H:%M:%S"), end.strftime("%d.%m.%Y %H:%M:%S")))

        cnx = db.connect(**DB_CONFIG, database='work')
        cursor = cnx.cursor()
        sql_begin = "SELECT * FROM work.test_descr WHERE "
        sql_stends = " or ".join(["stend_id={}".format(n) for n in stend_list])
        sql_date = "start > '{}' and start < '{}'".format(start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S"));

        sql = "SELECT COUNT(*) FROM work.test_descr WHERE ({}) and ({});".format(sql_stends, sql_date)
        cursor.execute(sql)
        rows = cursor.fetchall()
        print("found {} records\n".format(rows[0][0]))


        sql = "SELECT * FROM work.test_descr WHERE ({}) and ({});".format(sql_stends, sql_date)
        cursor.execute(sql)
        #rows = cursor.fetchall()
        #print("found {} records".format(cursor.rowcount))
        common_stat = {'ok':set(), 'fail':set(), 'repok':set(), 'rep':0, 'n':0}
        stat={}
        for stend in stend_list:
            stat[stend]={'ok':set(), 'fail':set(), 'repok':set(), 'rep':0, 'n':0}

        readed=0
        old_pers = 0

        row = cursor.fetchone()
        while row:
            mac = row[2]
            errors = row[6]
            stend = row[3]

            info = stat[stend]

            if (mac in info['ok']) or (mac in info['fail']):
                info['rep'] = info['rep'] + 1
            info['n'] = info['n'] + 1

            if (mac in common_stat['ok']) or (mac in common_stat['fail']):
                common_stat['rep'] = common_stat['rep'] + 1
            common_stat['n'] = common_stat['n'] + 1

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
            
            pers = readed / cursor.rowcount *100
            if pers != old_pers:
                print("{}%".format(int(pers)), end='\r')
                old_pers = pers

            row = cursor.fetchone()

        print("{:>9}{:>9}{:>9}{:>9}{:>9}{:>9}".format("STEND", "COUNT", "OK", "FAIL", "REPEATE", "FAIL&OK"))

        n=0
        ok=0
        fail=0
        rep=0
        repok=0
        for stend, info in stat.items():
            print("{:9}{:9}{:9}{:9}{:9}{:>9}".format(stend, info['n'], len(info['ok']), len(info['fail']), info['rep'], len(info['repok'])))
            n = n + info['n']
            ok = ok + len(info['ok'])
            fail = fail + len(info['fail'])
            rep = rep + info['rep']
            repok = repok + len(info['repok'])

        print('---------'*6)
        print("{:9}{:9}{:9}{:9}{:9}{:>9}".format('ALL', n, ok, fail, rep, repok))
        print('---------'*6)
        print("{:9}{:9}{:9}{:9}{:9}{:>9}".format('COMMON', common_stat['n'], len(common_stat['ok']), len(common_stat['fail']), common_stat['rep'], len(common_stat['repok'])))
        input("\npress enter to exit")