import mysql.connector as db
import re
import codecs

from src.assembly_point__old_web.env import DB_CONFIG

STEND = 89
START = '2020-02-02 00:00:00'
END = '2020-04-02 12:00:00'
ONLY_OK = True


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
    with codecs.open("plc_7V_stend_{}_{}.xml".format(STEND, 'ok' if ONLY_OK else 'full'), "w", "utf-8") as f:        
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
            quals=re.findall("Напряжение PLC тракта: (-?\d+\.?\d*)", row[8])

            'Quality: 723.88060'
            f.write('<Row>\n')

            f.write('''<Cell><Data ss:Type="String">{}</Data></Cell>\n'''.format(row[0]))
            for value in quals:                  
                f.write('''<Cell><Data ss:Type="String">{}</Data></Cell>\n'''.format(str(value).replace('.',',')))
            f.write('</Row>\n')
            row = cursor.fetchone()
        cnx.close()
        f.write(end_xml)