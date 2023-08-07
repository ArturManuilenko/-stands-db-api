from reportlab.platypus.flowables import Flowable

from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus.tables import Table, TableStyle

import reportlab.platypus.paragraph as paragraph
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.units import cm, mm

from reportlab.lib.styles import ParagraphStyle

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import reportlab.lib.colors as colors

from reportlab.platypus import PageBreak, Spacer

from reportlab.pdfgen import canvas

# init reportlab 

pdfmetrics.registerFont(TTFont('Times New Roman', 'report_verification/times-new-roman.ttf'))
pdfmetrics.registerFont(TTFont('Times New RomanB', 'report_verification/times-new-roman-gras.ttf'))
pdfmetrics.registerFont(TTFont('Times New RomanI', 'report_verification/times-new-roman-italique.ttf'))
pdfmetrics.registerFont(TTFont('Times New RomanBI', 'report_verification/times-new-roman-gras-italique.ttf'))

pdfmetrics.registerFontFamily('Times New Roman',normal='Times New Roman',
                              bold='Times New RomanB',italic='Times New RomanI',boldItalic='Times New RomanBI')

pstyle = ParagraphStyle('base',
                        alignment=paragraph.TA_LEFT,
                        fontSize=10,
                        fontName="Times New Roman")

pstyle_hdr = ParagraphStyle('base1',
                        alignment=paragraph.TA_CENTER,
                        fontSize=10,
                        fontName="Times New Roman")


class FooterCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_canvas(page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_canvas(self, page_count):
        self.saveState()
        self.setStrokeColorRGB(0, 0, 0)
        self.setLineWidth(0.5)
        self.line(10*mm, 13*mm, A4[0] - 10*mm, 13*mm)
        self.setFont('Times New Roman', 10)
        self.drawString(A4[0] - 20*mm, 5*mm, '{}'.format(self._pageNumber))
        self.restoreState()





#
def page_break():
    return PageBreak()

def spacer(h):
    return Spacer(0,h)

def page_header(num, type):
    return Paragraph('<b>Протокол государственной поверки № {} <br/> счетчиков электрической энергии однофазных Тип: {}</b>'.format(num, type),pstyle_hdr)

def page_header1(num, descr, type):
    return Paragraph('<b>Протокол государственной поверки № {} <br/> {} <br/> Тип: {}</b>'.format(num, descr, type),pstyle_hdr)

def page_header_ex(lines):
    return Paragraph('{}'.format('<br/>'.join(lines)),pstyle_hdr)

def text(txt, style=pstyle):
    return Paragraph(txt, style)

col_tbl_style = TableStyle([
    ('FONT', (0, 0), (-1, -1), 'Times New Roman', 10),
    #('GRID',(0,0),(-1,-1),0.5,colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ])

def org_info(customer, lab, place):
    tdata = (
        ('Наименование организации\nзаказчика:',customer),
        ('Наименование организации,\nпроводившей государственную\nповерку:',lab),
        ('Место проведения\nгосударственной поверки:',place)
        )
    t=Table(tdata,colWidths=[50*mm, 160*mm], hAlign='LEFT')
    t.setStyle(col_tbl_style)
    return t

mon=['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря']
def report_info(date, tnpa):

    date_text = '{:02d} {} {:04d}г.'.format(date.day, mon[date.month-1], date.year)

    tdata = [[
        Paragraph('Дата государственной\nповерки: <b>{}</b>'.format(date_text), pstyle),
        Paragraph('Наименование и обозначение ТНПА: <b>{}</b>'.format(tnpa), pstyle)
         ]]
    t=Table(tdata,colWidths=[50*mm, 160*mm], hAlign='LEFT')
    t.setStyle(col_tbl_style)
    return t

def unit_info(descr):
    tdata = [['Эталонное оборудование:',descr]]
    t=Table(tdata,colWidths=[50*mm, 200*mm], hAlign='LEFT')
    t.setStyle(col_tbl_style)
    return t

def measure_info(t, f ,p):
    descr= Paragraph('температура окружающего воздуха <b>{} °С</b><br/>относительная влажность воздуха <b>{} %</b><br/>атмосферное давление <b>{} кПА</b>'.format(t,f,p), pstyle)
    tdata = [['Условия проведения\nгосударственной поверки: ',descr]]
    t=Table(tdata,colWidths=[50*mm, 200*mm], hAlign='LEFT')
    t.setStyle(col_tbl_style)
    return t





text_table_style = TableStyle([
   ('FONT', (0, 0), (-1, -1), 'Times New Roman', 10),
   ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
   ('VALIGN', (0, 0), (-1, -1), 'TOP'),
   ('LEFTPADDING', (0, 0), (-1, -1), 0),
   ('RIGHTPADDING', (0, 0), (-1, -1), 0),
   ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
   ('TOPPADDING', (0, 0), (-1, -1), 0),
        ])
def add_text_table(data, width=None):
    tdata = [[Paragraph(cell, pstyle) for cell in row] for row in data]
    t=Table(tdata,colWidths=width, hAlign='LEFT')
    t.setStyle(text_table_style)
    return t

def add_text(text):
    return add_text_table([[text]], [180*mm])

    descr= Paragraph(s, pstyle)
    tdata = [[descr]]
    t=Table(tdata,colWidths=[180*mm], hAlign='LEFT')
    t.setStyle(col_tbl_style)
    return t

def add_text2(text):
    p = Paragraph(text, pstyle)
    return p

def signature(fio):
    col_tbl_style = TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Times New Roman', 10),
        ('FONT', (0, 3), (-1, 3), 'Times New Roman', 8),
        #('GRID',(0,0),(-1,-1),0.5,colors.black),
        ('ALIGN', (0, 0), (0, 3), 'LEFT'),
        ('ALIGN', (-1, 0), (-1, 3), 'RIGHT'),
        ('ALIGN', (1, 3), (1, 3), 'CENTER'),
        ('LINEABOVE',(1,3),(1,3),1,colors.black)
    ])
    tdata = [
        ['Заключение: годны','',''],
        ['Поверку провел:','',''],
        ['Государственный поверитель','',fio],
        ['','(подпись)','']
        ]
    t=Table(tdata,colWidths=[70*mm,50*mm,70*mm], hAlign='LEFT', repeatRows=4)
    t.setStyle(col_tbl_style)
    return t

def signature1(name, fio):
    col_tbl_style = TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Times New Roman', 10),
        ('FONT', (0, 1), (-1, 1), 'Times New Roman', 8),
        #('GRID',(0,0),(-1,-1),0.5,colors.black),
        ('ALIGN', (0, 0), (0, 1), 'LEFT'),
        ('ALIGN', (-1, 0), (-1, 1), 'RIGHT'),
        ('ALIGN', (1, 1), (1, 1), 'CENTER'),
        ('LINEABOVE',(1,1),(1,1),1,colors.black)
    ])
    tdata = [
        [name,'',fio],
        ['','(подпись)','']
        ]
    t=Table(tdata,colWidths=[70*mm,50*mm,70*mm], hAlign='LEFT', repeatRows=2)
    t.setStyle(col_tbl_style)
    return t

def data_table(data, width, style, **kvarg):
    t=Table(data, colWidths = width, hAlign='LEFT', **kvarg)
    t.setStyle(TableStyle(style))
    return t

def add_block(res, block, **param):
    b,s,w = res
    b1,s1,w1 = block(len(w), **param)
    for i in range(len(b)):
        b[i].extend(b1[i])
    s.extend(s1)
    w.extend(w1)

class Footer():
    def __init__(self, numbers = False, text = ''):
        self.text = text
        self.numbers = numbers

    def __call__(self, canvas, document):
        canvas.saveState()
        canvas.setStrokeColorRGB(0, 0, 0)
        canvas.setLineWidth(0.5)
        canvas.line(10*mm, 13*mm, A4[0] - 10*mm, 13*mm)
        canvas.setFont('Times New Roman', 10)
        if self.text != '':
            canvas.drawString(10*mm, 5*mm, self.text)
        if self.numbers:
            canvas.drawString(A4[0] - 20*mm, 5*mm, '{}'.format(document.page))
        canvas.restoreState()

class Report:
    def __init__(self, file, pageNumbers=False, footer = '', info = {}):
        self.file = file
        self.elements=[]
        self.pageNumbers = pageNumbers
        self.footer = footer
        self.info = info

    def add_protocol(self):
        self.devs = []

        if len(self.elements) > 0:
           self.elements.append(page_break())

    def addHeader(self):
        pass

    def addDevice(self, mac, place, measures):
        self.devs.append((mac, place + 1, measures))

    def endProtocol(self, fio):
        pass



    def save(self):
        doc = SimpleDocTemplate(self.file, pagesize=A4, #landscape(A4),
                leftMargin=10*mm,
                rightMargin=10*mm,
                topMargin=10*mm,
                bottomMargin=15*mm)

        ftr = Footer(self.pageNumbers, self.footer)
        doc.build(self.elements, onFirstPage=ftr, onLaterPages=ftr)