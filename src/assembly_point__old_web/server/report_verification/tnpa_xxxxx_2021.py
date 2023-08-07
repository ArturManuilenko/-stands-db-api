import reportlab.lib.colors as colors
from report_verification.vtext import vtext
import report_verification.base_report as base_report

MAC_W = 86.0
PAGE_W = 535.0
DATA_W = PAGE_W - MAC_W

algoritms = {
    'Metano A - G1,6 RF':{'model':'Metano A – G1,6 RF', 'name':'МРБ МП.3108-2021', 'qmin':0.016, 'qmax':2.500},
    'Metano A - G2,5 RF':{'model':'Metano A – G2,5 RF', 'name':'МРБ МП.3108-2021', 'qmin':0.025, 'qmax':4.000},
    'Metano A - G4,0 RF':{'model':'Metano A – G4,0 RF', 'name':'МРБ МП.3108-2021', 'qmin':0.040, 'qmax':6.000},
    'Metano A - G6,0 RF':{'model':'Metano A – G6,0 RF', 'name':'МРБ МП.3108-2021', 'qmin':0.060, 'qmax':10.000},
}

def base_block():
    return (
        [
            [vtext('№ п/п'),vtext('№ места'), '№ счетчика'],
        ],
        [
            ('FONT', (0, 0), (-1, -1), 'Times New Roman', 8),
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('BACKGROUND',(0,0),(1,1),colors.white),
        ],
        [18,18,50]      
        )

def result_block(col):
    return (
        [
            ['Внешний осмотр',
             'Опробование, проверка правильности, работы счётного механизма,\nиспытательных выходов, работоспособности радиоинтерфейса',
             'Герметичность'],
        ],
        [
            ('FONT', (0, 0), (-1, -1), 'Times New Roman', 8),
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('BACKGROUND',(0,0),(1,1),colors.white),
            
        ],
        [80, DATA_W - 80*2, 80]
        )




def measure_block(col):
    return (
        [
            [vtext('Порог чувствительности'),
            vtext('Расход воздуха,\n(Q), м³/ч'),
            vtext('Объём воздуха,\nизмеренный счётчиком\n(Uс), м³'),
            vtext('Объём воздуха,\nзадаваемый установкой\n(U1), м³'),
            vtext('Потеря давления\nна счётчике,\n(ΔР), %'),
            vtext('Основная относительная\nпогрешность поверяемого\nсчётчика\n(σ), %'),
            vtext('Допускаемая основная\nотносительная погрешность\n(σ доп), %')],
        ],
        [
            ('FONT', (0, 0), (-1, -1), 'Times New Roman', 8),
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('BACKGROUND',(0,0),(1,1),colors.white),            

            ('VALIGN', (0, 1), (-1, -1), 'MIDDLE')
        ],
        [DATA_W / 7]*7
        )

def add_block(res, block, **param):
    b,s,w = res
    b1,s1,w1 = block(len(w), **param)
    for i in range(len(b)):
        b[i].extend(b1[i])
    s.extend(s1)
    w.extend(w1)

def tnpa_xxxxx_2021_result(data):
    res = base_block()
    add_block(res, result_block)

    header, style, width = res
    n = 0
    for mac, place, m in data:
        n += 1
        row = [str(n), str(place), str(mac), 'годен', 'годен', 'см.приложение']
        header.append(row)
    return base_report.data_table(header, width, style, repeatRows=1)

def tnpa_xxxxx_2021_measure(data, qmin, qmax):
    res = base_block()
    add_block(res, measure_block)

    descr = (
        (1,'min',3),
        (3,'min',3),
        (0.1,'max',1.5),
        (0.2,'max',1.5),
        (0.4,'max',1.5),
        (0.7,'max',1.5),
        (1,'max',1.5)
        )

    header, style, width = res
    n = 0
    for mac, place, m in data:
        style.append( ('SPAN',(0, 7 * n + 1),(0, 7 * n + 7)) )
        style.append( ('SPAN',(1, 7 * n + 1),(1, 7 * n + 7)) )
        style.append( ('SPAN',(2, 7 * n + 1),(2, 7 * n + 7)) )
        style.append( ('SPAN',(3, 7 * n + 1),(3, 7 * n + 7)) )

        style.append( ('SPAN',(9, 7 * n + 1),(9, 7 * n + 2)) )
        style.append( ('SPAN',(9, 7 * n + 3),(9, 7 * n + 7)) )
        n += 1        

        for k, val_type, dop in descr:
            row = [str(n), str(place), str(mac)]

            val = m.get('- V start')
            if val is not None:         
                #row.append('{:.2f}'.format(val['value']))
                row.append('годен' if val['result'] else 'не годен')
            else:
                row.append('')

            row.append('{:.3f} ({}Q{})'.format((qmin if val_type=='min' else qmax) *  k, k if k!=1 else '', val_type))

            Vval = m.get('- V {}Q{}'.format(k if k!=1 else '', val_type))
            dPval = m.get('- dP {}Q{}'.format(k if k!=1 else '', val_type))

            if Vval is not None:
                row.append('{:.5f}'.format(Vval['value']))
                row.append('{:.5f}'.format(Vval['etalon']))               
            else:
                row.append('')
                row.append('')

            if dPval is not None:         
                row.append('{:.2f}'.format(dPval['error']))
            else:
                row.append('')

            if Vval is not None:         
                row.append('{:.2f}'.format(Vval['error']))
            else:
                row.append('')

            row.append('{:.1f}'.format(dop))
            header.append(row)
    return base_report.data_table(header, width, style, repeatRows=1)


class tnpa_xxxxx_2021(base_report.Report):
    algoritm = algoritms.keys()

    def __init__(self, *args, **kwargs):
        res = super().__init__(*args, pageNumbers = True, 
                               footer = '№ {}-СГУ/{}'.format(kwargs['info']['id'],kwargs['info']['time'].year), 
                               **kwargs)
        return res
    
    def addProtocol(self, number, model, customer, lab_name, lab_descr, place, date, unit, t, f, p):
        self.add_protocol()

        self.tnpa = algoritms[model]
        self.elements.extend([
            base_report.page_header1(number, 'счётчиков газа ультразвуковых', self.tnpa['model']),
            base_report.org_info(customer, lab_descr, place),
            base_report.report_info(date, self.tnpa['name']),
            base_report.unit_info(unit),
            base_report.measure_info(t, f, p),
            base_report.add_text('1. Результаты поверки:'),
            ])

    def endProtocol(self, fio):
        self.elements.append(tnpa_xxxxx_2021_result(self.devs))
        self.elements.append(base_report.add_text('2. Определение метрологических характеристик'))
        self.elements.append(tnpa_xxxxx_2021_measure(self.devs, self.tnpa['qmin'], self.tnpa['qmax']))
              
        self.elements.append(base_report.signature(fio))