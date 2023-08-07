import mysql.connector as db
import datetime
import codecs

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

def report(task, number):
    if type(number) is int:
        number = [number]

    cond = ' or '.join(['test_id={}'.format(n) for n in number])
    cnx = db.connect(**DB_CONFIG, database='work')
    cursor = cnx.cursor()
    sql = "SELECT string FROM work.full_report WHERE {};".format(cond)
    cursor.execute(sql)
    rows = cursor.fetchall()

    strs = [r[0] for r in rows]     
    return  '\n\n{}\n\n'.format(80 * '*').join(strs)

if __name__ == "__main__":
    number = int(input("enter report number\n>"))
    
    data = report(EmptyTask(), number)
    print(data)

    input("\npress enter to exit")