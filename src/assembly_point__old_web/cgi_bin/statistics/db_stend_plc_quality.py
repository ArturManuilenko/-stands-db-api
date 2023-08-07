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
    stend = 70
    start = '2018-10-30 00:00:00'
    end = '2018-10-31 18:00:00'
    with codecs.open("plc_quality_stend_{}.xml".format(stend), "w", "utf-8") as f:        
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
            quals=re.findall("(гармоника 57...> +((\d+); +)+)", row[8])

            quals_data = []
            for q in quals:
                quals_data.append([int(i) for i in re.findall("\d+", q[0])])
            
            if len(quals_data) != 12 and len(quals_data) != 24: 
                row = cursor.fetchone()
                continue
            #quals_data = quals_data[:-1]
            'Quality: 723.88060'
            f.write('<Row>\n')

            f.write('''<Cell><Data ss:Type="String">{}</Data></Cell>\n'''.format(row[0]))

            for i in range(12):
                q = quals_data[i]
                f.write('''<Cell><Data ss:Type="String">{}</Data></Cell>\n'''.format(q[i+3]))
            f.write('</Row>\n')
            if len(quals_data) == 24:
                f.write('<Row>\n')
                f.write('''<Cell><Data ss:Type="String">{}</Data></Cell>\n'''.format('-'))
                for i in range(12):
                    q = quals_data[12+i]
                    f.write('''<Cell><Data ss:Type="String">{}</Data></Cell>\n'''.format(q[i+3]))

                f.write('</Row>\n')

            row = cursor.fetchone()
        cnx.close()
        f.write(end_xml)