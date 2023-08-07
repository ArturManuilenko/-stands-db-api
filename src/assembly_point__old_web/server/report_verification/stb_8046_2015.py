import reportlab.lib.colors as colors

from reportlab.platypus import Image
from reportlab.platypus.tables import  Table, TableStyle
from reportlab.lib.units import mm

from src.assembly_point__old_web.server.report_verification import base_report

MAC_W = 20*mm
PAGE_W = 550.0
DATA_W = PAGE_W - MAC_W

algoritms = {
    'FLUO+WENLING_Q1,6_R20':
    {'model':'SM', 'name':'FLUO-1.1 R20 (Q3=1,6 м³/ч)', 'R':20, 'Q3':'1.6', 'Q2':'0.128', 'Q1':'0.08'},
    'FLUO+WENLING_Q1,6_R100':
    {'model':'SM', 'name':'FLUO-1.1 R100 (Q3=1,6 м³/ч)', 'R':100, 'Q3':'1.6', 'Q2':'0.026', 'Q1':'0.016'},
    'FLUO+WENLING_Q1,6_R50':
    {'model':'SM', 'name':'FLUO-1.1 R50 (Q3=1,6 м³/ч)', 'R':50, 'Q3':'1.6', 'Q2':'0.051', 'Q1':'0.032'},
    'FLUO+WENLING_Q2,5_R20':
    {'model':'SM', 'name':'FLUO-1.1 R20 (Q3=2,5 м³/ч)', 'R':20, 'Q3':'2.5', 'Q2':'0.2', 'Q1':'0.125'},
    'FLUO+HUASHUN_Q1,6_R40':
    {'model':'SM', 'name':'FLUO-1.2 R40 (Q3=1,6 м³/ч)', 'R':40, 'Q3':'1.6', 'Q2':'0.064', 'Q1':'0.04'}
}

def base_block():
    return (
        [
            ['№\nп/п', 'Номер\nсчетчика'],
            ['',''],
            ['',''],
        ],
        [
            ('FONT', (0, 0), (-1, -1), 'Times New Roman', 7),
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('BACKGROUND',(0,0),(-1,-1),colors.white),
            #row 0
            ('SPAN',(0,0),(0,2)),
            ('SPAN',(1,0),(1,2)),
        ],
        [7*mm,13*mm]
        )

def block_measure(col, number, error, q):
    Qs=['3','2','1']
    return (
        [
            ['Расход {}: Q{} = {} м³/ч'.format(number+1, Qs[number], q), '', ''],
            ['Измеренное\nзначение\nобъема Vи, л', 'Эталонное\nзначение\nобъема Vэ, л', 'Относительная\nпогрешность\nизмерения, %'],
            ['Пределы допускаемой относительной погрешности ±{} %'.format(error), '', ''],
        ],
        [
            ('SPAN',(col+0,0),(col+2,0)),
            ('SPAN',(col+0,2),(col+2,2)),
            ('FONT', (col+0,2), (col+2,2), 'Times New Roman', 5.5),
        ],
        [17*mm,17*mm,19*mm]      
        )	

def block_result(col):
    return (
        [
            ['Результат'],
            [''],
            [''],
        ],
        [
            ('SPAN',(col+0,0),(col+0,2)),
        ],
        [15*mm]      
        )	

def block_radio(col):
    return (
        [
            ['Начальные значения\nобъема, переданные\nпо радиоканалу, л',
    'Конечные значения\nобъема, переданные\nпо радиоканалу, л',
    'Измеренное\nзначение объема\nпри передаче данных\nпо радиоканалу, л',
    'Эталонное значение\nобъема, л',
    'Погрешность\nизмерения  Δ, л',
    'Допускаемая\nпогрешность\nизмерения Δ, л'],
            ['']*6,
            ['']*6,
        ],
        [
            ('SPAN',(col+0,0),(col+0,2)),
            ('SPAN',(col+1,0),(col+1,2)),
            ('SPAN',(col+2,0),(col+2,2)),
            ('SPAN',(col+3,0),(col+3,2)),
            ('SPAN',(col+4,0),(col+4,2)),
            ('SPAN',(col+5,0),(col+5,2)),
        ],
        [DATA_W / 6]*6
        )

def block_germ(col):
    return (
        [
            ['Результат'],
            [''],
            [''],
        ],
        [
            ('SPAN',(col+0,0),(col+0,2)),
        ],
        [DATA_W ]
        )

hdr_tbl_style = TableStyle([
    ('FONT', (0, 0), (-1, -1), 'Times New Roman', 10),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (2, 0), (2, 0), 'BOTTOM'),
    ('VALIGN', (2, 0), (2, 0), 'BOTTOM'),
    ])

def page_header(lab_descr, number, date):
    date_text = '{:02d} {} {:04d}г.'.format(date.day, base_report.mon[date.month-1], date.year)
    text = '{}<br/><br/><b>Протокол №{}</b><br/>поверки счетчика воды крыльчатого FLUO-1<br/>от {}'.format(
        lab_descr.replace('\n','<br/>'), number, date_text)

    tdata = [[Image('report_verification/iso9001.jpg', width=20*mm, height=20*mm, kind='proportional'), 
         base_report.text(text, base_report.pstyle_hdr),
         Image('report_verification/belgim_iec17025.jpg', width=30*mm, height=30*mm, kind='proportional')]]
    t=Table(tdata,colWidths=[40*mm, 120*mm, 40*mm], hAlign='CENTER')
    t.setStyle(hdr_tbl_style)
    return t


def stb_8046_2015_data(data, Qs):
    res = base_block()
    n_measure=0
    for Q3, err in Qs:
        base_report.add_block(res, block_measure, number=n_measure, q=Q3.replace('.',','), error=err)
        n_measure+=1
    base_report.add_block(res, block_result)
    header, style, width = res
    n = 0
    for mac, place, m in data:
        n += 1
        row = [n, str(mac)]

        for Q3, err in Qs:
            val = m.get('- V Q' + Q3, None)
            if val != None:
                row.append('{:.3f}'.format(val['value']))
                row.append('{:.3f}'.format(val['etalon']))
                row.append('{:.2f}'.format(val['error']))
        if len(row)==11: row.append('годен')
        header.append(row)

    return base_report.data_table(header, width, style, repeatRows=3)

def stb_8046_2015_radio_data(data):
    res = base_block()
    base_report.add_block(res, block_radio)

    datalist = [
        ('- V Rstart', 'value'),
        ('- V Rend', 'value'),
        ('- dV R', 'value'),
        ('- dV R', 'etalon'),
        ('- dV R', 'error'),
    ]

    header, style, width = res
    n = 0
    for mac, place, m in data:
        n += 1
        row = [n, str(mac)]
        for id,type in datalist:
            val = m.get(id, None)
            row.append('{:.3f}'.format(val[type]) if val else '-')

        row.append('±1')
            
        header.append(row)

    return base_report.data_table(header, width, style, repeatRows=1)


def stb_8046_2015_germ(data):
    res = base_block()
    base_report.add_block(res, block_germ)

    header, style, width = res
    n = 0
    for mac, place, m in data:
        n += 1
        row = [n, str(mac), 'Соответствует']
        header.append(row)

    return base_report.data_table(header, width, style, repeatRows=1)
#--------------

class stb_8046_2015(base_report.Report):
    algoritm = algoritms.keys()

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)
    
    def addProtocol(self, number, model, customer, lab_name, lab_descr, place, date, unit, t, f, p):
        self.mparam = t, f, p
        self.unit = unit
        self.add_protocol()
        self.info = algoritms[model]
        self.protonumber = number
        self.protodate = '{:02d} {} {:04d}г.'.format(date.day, base_report.mon[date.month-1], date.year)
        q3 = float(self.info['Q3'])
        lim_min = '{:.2f}'.format(q3 / self.info['R'])
        lim_max = '{:.2f}'.format(q3 * 1.25)

        self.elements.extend([
            page_header(lab_descr, number, date),
            base_report.add_text('<br/><br/>'),
            base_report.add_text_table([
                    ['Тип:', self.info['name']],
                    ['Кому принадлежит:','ООО "Неро Электроникс";'],
                    ['Диапазон измерения:','от {} до {} м³/ч;'.format(lim_min, lim_max)],
                    ['Относительная погрешность:','δ= ±5.0 % (от Q1 до Q2 не вкл.);<br/>δ= ±2.0 % (от Q2 до Q4);'],
                    ['Организация, проводившая поверку:','БелГИМ'],
                    ['Место проведения поверки:', place],			
                    ['Методика поверки:', 'СТБ 8046-2015'],
                ], [65*mm, 120*mm])
            ])

    def endProtocol(self, fio):
        t, f, p = self.mparam
        tv = 0.0
        ntv = 0
        for _,_,m in self.devs:
            for k in m.keys():
                if '- t Q' in k: 
                    tv = tv + m[k]['value']
                    ntv += 1
        if ntv == 0:
            tv=0.0
        else:
            tv = tv/ntv
        self.elements.extend([
            base_report.add_text('Условия  проведения  поверки:'),
            base_report.add_text_table([
                    ['','температура окружающего воздуха:','{}°C'.format(t)],
                    ['','температура поверочной среды  (воды):','{}°C'.format(int(tv))],
                    ['','относительная влажность воздуха:','{}%'.format(f)],
                    ['','атмосферное давление:','{}кПа'.format(p)],
                ], [5*mm, 60*mm, 15*mm]),
            base_report.add_text('Эталонные и вспомогательные средства измерений:'),
            base_report.add_text_table([['', self.unit.replace('\n','<br/>')]], [5*mm,180*mm]),
            base_report.add_text('Опробование:'),
            base_report.add_text_table([['', '''1 Внешний осмотр: соответствует СТБ 8046-2015
<br/>2 Опробование: соответствует СТБ 8046-2015
<br/>2.1 Проверка герметичности: соответствует СТБ 8046-2015
<br/>2.2 Проверка работоспособности вспомогательных устройств (радиоканала): соответствует РЭ
<br/>3 Определение относительной погрешности измерений:
''']], [5*mm,180*mm]),
            base_report.spacer(5*mm)
            ])
        self.elements.append(stb_8046_2015_data(self.devs, [(self.info['Q3'],2),(self.info['Q2'],2),(self.info['Q1'],5)]))

        self.elements.append(base_report.add_text_table([['', '''<br/>4 Определение погрешности вспомогательных устройств (радиоканала) при передаче данных:''']], [5*mm,180*mm]))
        self.elements.append(stb_8046_2015_radio_data(self.devs))

        self.elements.extend([
            base_report.spacer(5*mm),
            base_report.add_text_table([
                ['Заключение о результатах поверки: ','количество счетчиков прошедших поверку: {}'.format(len(self.devs))]
                ], [70*mm,90*mm]),
            base_report.spacer(20*mm)
            ])        

        self.elements.append(base_report.signature(fio))

        self.elements.append(base_report.page_break())


        # отчет на герметичность

        self.elements.append(base_report.page_header_ex([
            'ООО «Неро Электроникс»',
            'ПРОТОКОЛ № {}'.format(self.protonumber),
            'проверки на герметичность счётчиков воды крыльчатых FLUO-1.1',
            'от {}'.format(self.protodate)
            ]))
        self.elements.append(base_report.add_text2('<br/><br/>Испытание проводится в соответствии с требованиями СТБ 8046 2015'\
            ' «Система обеспечения единства измерений Республики Беларусь. Счётчики холодной питьевой воды и горячей воды. '\
            'Методика поверки».'))

        self.elements.append(base_report.add_text_table([['', '''<br/>1 Используемое оборудование:''']], [5*mm,180*mm]))

        header, style, width = (
        [
            ['№\nп/п', 'Наименование','Обозначение','Характеристики','Дата поверки'],
            ['1','Опрессовочный насос','НА-40','-',''],
            ['2','Манометр (в составе насоса)','МТ-100','иапазон измерений 0-4 МРа, класс точности 1,5','3-й кв. 2021г.'],
        ],
        [
            ('FONT', (0, 0), (-1, -1), 'Times New Roman', 7),
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('BACKGROUND',(0,0),(-1,-1),colors.white),
        ],
        [7*mm, 65*mm, 25*mm, 65*mm, PAGE_W - (7+65+65+25)*mm]
        )
        self.elements.append(base_report.data_table(header, width, style, repeatRows=1))


        self.elements.append(base_report.add_text_table([['', '''<br/>2 Результаты проверки:''']], [5*mm,180*mm]))
        self.elements.append(stb_8046_2015_germ(self.devs))

        self.elements.extend([
            base_report.spacer(5*mm),
            base_report.add_text_table([
                ['Заключение: ','счётчики воды крыльчатые в количестве {} штук прошли проверку на герметичность с положительными результатами.'.format(len(self.devs))]
                ], [70*mm,90*mm]),
            base_report.spacer(20*mm)
            ])
        self.elements.append(base_report.signature1('Испытания проводил', '________________'))