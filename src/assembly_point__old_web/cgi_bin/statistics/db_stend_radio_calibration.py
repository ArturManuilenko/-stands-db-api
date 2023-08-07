import mysql.connector as db
import re

from src.assembly_point__old_web.env import DB_CONFIG

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
import codecs

if __name__ == "__main__":
    stend = 100
    start = '2021-03-26 00:00:00'
    end = '2021-03-29 13:54:00'
    with codecs.open("radio_quality_stend_{}.xml".format(stend), "w", "utf-8") as f:        
        f.write(header)
         
        cnx = db.connect(**DB_CONFIG, database='work')
        cursor = cnx.cursor()
        cursor.execute("""SELECT * FROM work.test_descr,work.full_report WHERE test_descr.id=full_report.test_id """\
        """ AND test_descr.stend_id={} AND start>'{}' AND end<'{}' ORDER by work.test_descr.id DESC;""".format(stend, start, end))
        row = cursor.fetchone()

        readed=0
        res=[]
        while row != None:
            res.append(row)
            quals=re.findall("Quality: (-?\d+\.?\d*)", row[8])

            calibr = re.findall("Калибровка генератора радио\n(?:OK        : 0.00000\n)*(?:OK        : (\d+\.\d+)\n)+", row[8])
#            quals = []
#            m = row[8].split('\n')
#            for l in m:
#                if (l.find("Quality: ") != -1):
#                    x = l.split("Quality: ")[1]
#                    if x.find('/') != -1:
#                        x = x.split('/')
#                        quals.append(x[0].strip())
#                        quals.append(x[1].strip().split(' ')[0])
#                    else:
#                        quals.append(x.split(' ')[0])

            'Quality: 723.88060'
            f.write('<Row>\n')

            f.write('''<Cell><Data ss:Type="String">{}</Data></Cell>\n'''.format(row[0]))
            f.write('''<Cell><Data ss:Type="String">{}</Data></Cell>\n'''.format(row[2]))
            for value in calibr:                  
                f.write('''<Cell><Data ss:Type="String">{}</Data></Cell>\n'''.format(str(value).replace('.',',')))

            for value in quals:                  
                f.write('''<Cell><Data ss:Type="String">{}</Data></Cell>\n'''.format(str(value).replace('.',',')))
            f.write('</Row>\n')
            row = cursor.fetchone()
        cnx.close()
        f.write(end_xml)