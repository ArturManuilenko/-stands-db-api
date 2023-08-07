import mysql.connector as db
import xlsxwriter

from src.assembly_point__old_web.env import DB_CONFIG


def energomera_report(task, dt_from, dt_to):
    cnx = db.connect(**DB_CONFIG, database='energomera')

    file = task.createFile('energomera.xlsx')
    workbook = xlsxwriter.Workbook(file)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})

    cols_width = [17.0, 6.0, 11.0, 35, 9.3, 6.5, 6.5]
    header_list = ["DATETIME (GMT)", "STEND", "MAC", "SERIAL", "VERSION", "RESULT", "DEVICE"]
    for i in range(len(header_list)):
        worksheet.set_column(i, i, cols_width[i])
        worksheet.write(0, i, header_list[i], bold)
        
    task.setProgress(0.1)

    cursor=cnx.cursor(dictionary=False)
    cursor.execute("SELECT COUNT(*) FROM `firm` "
                "WHERE `date`>=%s AND `date`<%s AND `rep`=0 AND `new`=1 AND `result`=1;", 
                (dt_from, dt_to)
                )
    count = cursor.fetchall()[0][0]

    cursor=cnx.cursor(dictionary=True)
    cursor.execute("SELECT `date`,`stend`,`mac`,`serial`,`version`,`result`,`rep`,`new` FROM `firm` "
                   "JOIN `mail` ON `mail`.`id`=`firm`.`mail`"
                "WHERE `date`>=%s AND `date`<%s AND `rep`=0 AND `new`=1 AND `result`=1 ORDER BY `date`;", 
                (dt_from, dt_to)
                )

    task.setProgress(0.2)

    readed = 0
    for row in cursor:
        readed+=1
        worksheet.write(readed, 0, row['date'].strftime('%d.%m.%Y %H:%M:%S'))
        worksheet.write(readed, 1, row['stend'])
        worksheet.write(readed, 2, int(row['mac']))
        worksheet.write(readed, 3, row['serial'])
        worksheet.write(readed, 4, row['version'])
        worksheet.write(readed, 5, 'OK' if row['result'] else 'FAIL')
        worksheet.write(readed, 6, 'NEW' if row['new']==1 and row['rep']==0 else 'EXIST')

        task.setProgress(0.2 + 0.8 * readed / count)

    workbook.close()

if __name__ == "__main__":
    from command_task import EmptyTask
    while True:
        dt_from = input("Enter date from (2000-01-01 00:00:00)> ")
        dt_to = input("Enter date to (2099-01-01 00:00:00)> ")
        if dt_from == '': 
            dt_from = '2000-01-01 00:00:00'
        if dt_to == '': 
            dt_to = '2099-01-01 00:00:00'
        energomera_report(EmptyTask(), dt_from, dt_to)

    input("\npress enter to exit")