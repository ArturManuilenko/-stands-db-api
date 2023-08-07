from report_verification.report import Report
import datetime

customer = '''ООО "Неро Электроникс". Адрес: Минская обл., Минский р-н, Новодворский с/с, 74, комн. 11,
район д. Королищевичи'''
lab = 'ПИО измерений электрических величин, БелГИМ. Адрес: г. Минск, Старовиленский тракт,93'
place = '''ООО "Неро Электроникс". Адрес: Минская обл., Минский р-н, Новодворский с/с, 74, комн. 11,
район д. Королищевичи'''	

report = Report('01-0001', '', customer, lab, place, datetime.datetime.now())



exit



from    reportlab.platypus.doctemplate  import  SimpleDocTemplate
from    reportlab.lib.pagesizes         import  A4, landscape
from    reportlab.platypus.tables       import  Table, TableStyle

import reportlab.platypus.paragraph as paragraph
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.units import cm,mm

from reportlab.lib.styles import ParagraphStyle
style = getSampleStyleSheet()
yourStyle = ParagraphStyle('yourtitle',
                           fontName="Times New Roman",
                           fontSize=10,
                           parent=style['Heading2'],
                           alignment=1,
                           spaceAfter=14)

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import reportlab.lib.colors as colors

import report_verification
from report_verification.vtext import vtext

pdfmetrics.registerFont(TTFont('Times New Roman', 'times-new-roman.ttf'))
pdfmetrics.registerFont(TTFont('Times New RomanB', 'times-new-roman-gras.ttf'))
pdfmetrics.registerFont(TTFont('Times New RomanI', 'times-new-roman-italique.ttf'))
pdfmetrics.registerFont(TTFont('Times New RomanBI', 'times-new-roman-gras-italique.ttf'))

pdfmetrics.registerFontFamily('Times New Roman',normal='Times New Roman',
                              bold='Times New RomanB',italic='Times New RomanI',boldItalic='Times New RomanBI')


style = ParagraphStyle('parrafos',
                                   alignment=paragraph.TA_LEFT,
                                   fontSize=10,
                                   fontName="Times New Roman")

doc = SimpleDocTemplate('form1.pdf',pagesize=landscape(A4), 
                    leftMargin=10*mm,
                    rightMargin=10*mm,
                    topMargin=10*mm,
                    bottomMargin=10*mm)

elements=[]
for i in range(20):
    elements.append(Paragraph('<b>Протокол поверки № __ - ________________ счетчиков электрической энергии однофазных Тип: SM204 5(100)А 1/1 Х.Х.Х.Х.Х.Х</b>',style))  

data = [
    ['№\nп/п', '№ счетчика', 
     vtext('Внешний осмотр'), vtext('Опробование'), vtext('Проверка электрической\nпрочности изоляции'),
     'Определение метрологических характеристик для активной энергии (фазный канал), 230В','','','','','','','','','','','','','','','',''],
     
    ['','','','','', vtext('Проверка\nчувствительности'),vtext('Проверка осутствия\nсамохода'),
      'Проверка суточного хода часов','','','cosϕ = 1','','','cosϕ = 0,5и','','','cosϕ = 0,8е','','','Iмакс','',''],
     
    ['','','','','','','',
     vtext('Измеренный\nпериод импульсов\nвремени, мкс'),
     vtext('Значение суточной\nкоррекции времени,\nустановленное\nв счетчике, с/сут'),
     vtext('Суточный ход\nчасов, с/сут'),
     'Ток, % Iϭ','','','','','','','','',
     vtext('cosϕ = 1'),vtext('cosϕ = 0,5и'),vtext('cosϕ = 0,8е')],
    ['','','','','','','','','','','5','10','100','10','20','100','10','20','100','','',''],
    ['','','','','','','','','','','±1,5','±1,0','±1,0','±1,5','±1,0','±1,0','±1,5','±1,0','±1,0','±1,0','±1,0','±1,0'],

    ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21'],
    #['Проверка<i>gggg</i>','Проверка'],
    #['03','04', vtext('123456789')]
    
    ]
for i in range(20):
    t=Table(data,colWidths=[20,60,20,20,30, 30,30, 40,50,40, 30,30,30, 30,30,30, 30,30,30, 30,30,30])
    tblstyle = TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Times New Roman', 8),
        ('GRID',(0,0),(-1,-1),0.5,0x000000),
        ('BACKGROUND',(0,0),(1,1),colors.white),
        #row 0
        ('SPAN',(0,0),(0,4)),
        ('SPAN',(1,0),(1,4)),
        ('SPAN',(2,0),(2,4)),
        ('SPAN',(3,0),(3,4)),
        ('SPAN',(4,0),(4,4)),
        ('SPAN',(5,0),(21,0)),
        #row 1
        ('SPAN',(5,1),(5,4)),
        ('SPAN',(6,1),(6,4)),
        ('SPAN',(7,1),(9,1)),
        ('SPAN',(10,1),(12,1)),
        ('SPAN',(13,1),(15,1)),
        ('SPAN',(16,1),(18,1)),
        ('SPAN',(19,1),(21,1)),
        #row 2
        ('SPAN',(7,2),(7,4)),
        ('SPAN',(8,2),(8,4)),
        ('SPAN',(9,2),(9,4)),
        ('SPAN',(10,2),(18,2)),

        ('SPAN',(19,2),(19,3)),
        ('SPAN',(20,2),(20,3)),
        ('SPAN',(21,2),(21,3)),    
        ])  
    t.setStyle(tblstyle)
    elements.append(t)  

doc.build(elements)


if __name__ == "__main__":
    pass