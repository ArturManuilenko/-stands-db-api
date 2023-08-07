from report_verification.report import Document
import datetime
import mysql.connector as db
import mysql.connector.cursor
import time

from src.assembly_point__old_web.env import DB_CONFIG

customer = '''ООО "Неро Электроникс". Адрес: Минская обл., Минский р-н, Новодворский с/с 74
комн. 11, район д. Королищевичи'''

def protocol_verification(task, ids):
    file = task.createFile('protocol.pdf')
    doc = Document(file)

    #report = Report(file)
    
    progress_id = 1.0 / len(ids)
    progress_com = 0.0
    for id in ids:
        conn = db.connect(**DB_CONFIG, database='calibration', connection_timeout = 5.0, autocommit=True)
        cursor = conn.cursor(dictionary=True, buffered=True)

        cursor.execute('SELECT `report` FROM `protocol_reports` WHERE `protocol`=%s;',(id,) );
        reports = [row['report'] for row in cursor.fetchall()]

        if len(reports) == 0: task.setError('Протокол не найден')

        cursor.execute("SELECT `number`,`fio`,`t`,`f`,`p`,`descr`,`name`,`time` FROM `protocol` p JOIN laboratory l ON l.id = p.lab WHERE p.id=%s;",(id,) );
        rows = cursor.fetchall()
        if len(rows) == 0: task.setError('Протокол не найден')
        r = rows[0]
        number,fio,t,f,p,lab_descr,lab_name,protocol_time = r['number'],r['fio'],r['t'],r['f'],r['p'],r['descr'],r['name'],r['time']

        task.setProgress(progress_com + 0.1 * progress_id)
        
        launch = None
        devs = []
        cursor.execute("SELECT id,launch,place,mac,result FROM `report` WHERE id IN({});".format(','.join([str(id) for id in reports])));
        for row in cursor.fetchall():
            if row['result'] != '000-ok': task.setError('В списке есть счетчики, не прошедшие поверку')
            if launch == None:
                launch = row['launch']
            #elif launch != row['launch']: task.setError('Счетчики из разных партий')

            measures = {}
            cursor1 = conn.cursor(dictionary=True, buffered=True)
            cursor1.execute('SELECT `group`,`type`,`phase`,`error`,`value`,`etalon`,`result` FROM `measure` WHERE `report`=%s;',(row['id'],) );
            for m_row in cursor1.fetchall():
                measures[m_row['phase'] + ' ' + m_row['group'] + ' ' + m_row['type']] = {k: m_row[k] for k in ['error','value','etalon','result']}            

            devs.append((row['mac'], row['place'], measures))

        task.setProgress(progress_com + 0.8 * progress_id)
        cursor.execute('SELECT l.end, i.place, i.descr, a.name, a.stage_count FROM launch l '\
            'JOIN unit_info i ON l.unit_info=i.id '\
            'JOIN algoritm a ON a.id=l.algoritm '\
            'WHERE l.id=%s;',(launch,) );

        rows = cursor.fetchall()
        if len(rows) == 0: task.setError('Информация о партии отсутствует')
        r = rows[0]
        #self, number, model, customer, lab, place, date, unit, t, f, p

        report = doc.add_report(r['name'], id, protocol_time)
        report.addProtocol(number, r['name'], customer, lab_name, lab_descr, r['place'], r['end'], r['descr'], t, f, p)

        for mac, place, measures in devs:
            report.addDevice(mac, place,measures)        
        
        task.setProgress(progress_com + 0.9 * progress_id)
        report.endProtocol(fio)
        progress_com += progress_id

    report.save()

if __name__ == "__main__":
    from command_task import EmptyTask
    while True:
        n = input("Enter protocol number> ")
        data = protocol_verification(EmptyTask(), [n])
        print(data)

    input("\npress enter to exit")