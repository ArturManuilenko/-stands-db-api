import mysql.connector as db

import codecs
import re

from src.assembly_point__old_web.env import DB_CONFIG

file = 'battery.tsv'
start = '2020-06-11 06:00:00'
end = '2020-07-16 00:00:00'
errors = 1000
stends = [100, 101, 102, 103, 104, 106, 107, 108]

if __name__ == "__main__":
    with codecs.open(file, "w", "utf-8") as f:
        cnx = db.connect(**DB_CONFIG, database='work')
        cursor = cnx.cursor()
        cursor.execute("""SELECT * FROM work.test_descr,work.full_report"""
                        """ WHERE test_descr.id=full_report.test_id AND test_descr.start > '{}' AND test_descr.end < '{}'"""
                        """ AND stend_id IN ({}) AND errors<{} ORDER BY work.test_descr.id DESC;""".format(start, end, ','.join([str(st) for st in stends]), errors+1))

        print("fetching")

        f.write('STEND\tMAC\tDATE\n')

        r = cursor.fetchone()
        n = nd = 0
        while r:
            text = r[8]

            res = re.findall('Ток батареи: (\d\.\d+)\n', text)
            if len(res):
                f.write(str(r[3])+'\t')
                f.write(str(r[2])+'\t')
                f.write(r[4].strftime('%Y-%m-%d %H:%M:%S')+'\t')
                f.write('\t'.join([s.replace('.', ',') for s in res])+'\n')
                nd += 1
            else:
                l = ''
                pass

            if n % 100 == 0:
                print("get: {} check: {}".format(nd, n))
            n += 1
            r = cursor.fetchone()
