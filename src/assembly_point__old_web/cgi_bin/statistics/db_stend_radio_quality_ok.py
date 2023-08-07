import mysql.connector as db
import re
import codecs

from src.assembly_point__old_web.env import DB_CONFIG

STEND = 103
START = '2020-11-09 00:30:00'
END = '2020-11-09 23:00:00'
ONLY_OK = False


header='''
<?xml version="1.0" encoding="UTF-8"?>
<?mso-application progid="Excel.Sheet"?>
<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet"
xmlns:o="urn:schemas-microsoft-com:office:office"
xmlns:x="urn:schemas-microsoft-com:office:excel"
xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet"
xmlns:html="http://www.w3.org/TR/REC-html40">
<Worksheet ss:Name="Table1">
<Table>
'''

end_xml='''
</Table>
</Worksheet>
</Workbook>
'''

if __name__ == "__main__":
    with codecs.open("radio_quality_stend_{}_{}.xml".format(STEND, 'ok' if ONLY_OK else 'full'), "w", "utf-8") as f:        
        f.write(header)
         
        cnx = db.connect(**DB_CONFIG, database='work')
        cursor = cnx.cursor()

        ok_cond = 'AND test_descr.errors=0 ' if ONLY_OK else ''
        sql = '''SELECT * FROM work.test_descr,work.full_report '''\
            '''WHERE test_descr.id=full_report.test_id ''' + ok_cond +\
            ''' AND test_descr.stend_id=%s AND start>%s AND end<%s ORDER by work.test_descr.id DESC;'''
        cursor.execute(sql, (STEND, START, END))
        row = cursor.fetchone()

        readed=0
        res=[]
        while row != None:
            res.append(row)
#            quals=re.findall("Quality: (-?\d+\.?\d*)", row[8])
            quals = []
            m = row[8].split('\n')
            for l in m:
                if (l.find("Quality: ") != -1):
                    x = l.split("Quality: ")[1]
                    if x.find('/') != -1:
                        x = x.split('/')
                        quals.append(x[0].strip())
                        quals.append(x[1].strip().split(' ')[0])
                    else: #если не нужно значение проверки радио в интро
                        quals.append(x.split(' ')[0]) #если не нужно значение проверки радио в интро

            'Quality: 723.88060'
            f.write('<Row>\n')

            f.write('''<Cell><Data ss:Type="String">{}</Data></Cell>\n'''.format(row[0]))
            for value in quals:                  
                f.write('''<Cell><Data ss:Type="String">{}</Data></Cell>\n'''.format(str(value).replace('.',',')))
            f.write('</Row>\n')
            row = cursor.fetchone()
        cnx.close()
        f.write(end_xml)