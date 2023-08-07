import reportlab.lib.colors as colors

import src.assembly_point__old_web.server.report_verification.base_report as base_report
from src.assembly_point__old_web.server.report_verification.vtext import vtext

MAC_W = 86.0
PAGE_W = 535.0
DATA_W = PAGE_W - MAC_W

tnpa_list = {
    'SM204 5-60 L AR':{'model':'SM', 'name':'МРБ МП.2948-2020', 'R':True, 'N':False, 'gen':True},
    'SM204 5-100 L AR':{'model':'SM', 'name':'МРБ МП.2948-2020', 'R':True, 'N':False, 'gen':True},
    'SM204 5-60 L A':{'model':'SM', 'name':'МРБ МП.2948-2020', 'R':False, 'N':False, 'gen':True},
    'SM204 5-100 L A':{'model':'SM', 'name':'МРБ МП.2948-2020', 'R':False, 'N':False, 'gen':True},
    'SM204 5-60 LN AR':{'model':'SM204 5(60)А 1/1 D.O.RF.L', 'name':'МРБ МП.2948-2020', 'R':True, 'N':True, 'gen':True},
    'SM204 5-100 LN AR':{'model':'SM204 5(100) 1/1 D.R.O.RF.L', 'name':'МРБ МП.2948-2020', 'R':True, 'N':True, 'gen':True},
    'SM204 5-60 LN A':{'model':'SM204 5(60) 1 D.R.O.RF.L', 'name':'МРБ МП.2948-2020', 'R':False, 'N':True, 'gen':True},
    'SM204 5-100 LN A':{'model':'SM204 5(100) 1 D.R.O.RF.L', 'name':'МРБ МП.2948-2020', 'R':False, 'N':True, 'gen':True},

    'SM204 5-60 L A+R+':{'model':'SM', 'name':'МРБ МП.2948-2020', 'R':True, 'N':False, 'gen':False},
    'SM204 5-100 L A+R+':{'model':'SM', 'name':'МРБ МП.2948-2020', 'R':True, 'N':False, 'gen':False},
    'SM204 5-60 L A+':{'model':'SM', 'name':'МРБ МП.2948-2020', 'R':False, 'N':False, 'gen':False},
    'SM204 5-100 L A+':{'model':'SM', 'name':'МРБ МП.2948-2020', 'R':False, 'N':False, 'gen':False},
    'SM204 5-60 LN A+R+':{'model':'SM 204 5(60) 1/1 R.O.RF.L', 'name':'МРБ МП.2948-2020', 'R':True, 'N':True, 'gen':False},
    'SM204 5-100 LN A+R+':{'model':'SM 204 5(100) 1/1 R.O.RF.L', 'name':'МРБ МП.2948-2020', 'R':True, 'N':True, 'gen':False},
    'SM204 5-60 LN A+':{'model':'SM204 5(60) 1 R.O.RF.L', 'name':'МРБ МП.2948-2020', 'R':False, 'N':True, 'gen':False},
    'SM204 5-100 LN A+':{'model':'SM204 5(100) 1 R.O.RF.L', 'name':'МРБ МП.2948-2020', 'R':False, 'N':True, 'gen':False}
}

def base_block():
    return (
        [
            [vtext('№ п/п'),vtext('№ места'), '№ счетчика'],
            ['','',''],
            ['','',''],
            ['','',''],
            ['','',''],
            ['','',''],
        ],
        [
            ('FONT', (0, 0), (-1, -1), 'Times New Roman', 8),
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('BACKGROUND',(0,0),(1,1),colors.white),
            #row 0
            ('SPAN',(0,0),(0,5)),
            ('SPAN',(1,0),(1,5)),
            ('SPAN',(2,0),(2,5)),
        ],
        [18,18,50]      
        )

def base_block5():
    return (
        [
            [vtext('№ п/п'),vtext('№ места'), '№ счетчика'],
            ['','',''],
            ['','',''],
            ['','',''],
            ['','','']
        ],
        [
            ('FONT', (0, 0), (-1, -1), 'Times New Roman', 8),
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('BACKGROUND',(0,0),(1,1),colors.white),
            #row 0
            ('SPAN',(0,0),(0,4)),
            ('SPAN',(1,0),(1,4)),
            ('SPAN',(2,0),(2,4)),
        ],
        [18,18,50]      
        )

def extra_block():
    return (
        [
            [vtext('№ п/п'), vtext('№ места'), '№ счетчика','№ клейма-наклейки'],
        ],
        [
            ('FONT', (0, 0), (-1, -1), 'Times New Roman', 8),
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('BACKGROUND',(0,0),(1,1),colors.white),
        ],
        [18,18,50,DATA_W]   
        )

def block_common(col):
    return (
        [
            ['Внешний\nосмотр', 'Проверка\nэлектрической\nпрочности\nизоляции','Опробование',
             'Проверка\nчувствительности','Проверка\nосутствия\nсамохода'],
            ['','','','',''],
            ['','','','',''],
            ['','','','',''],
            ['','','','',''],
            ['','','','','']
        ],
        [
            ('SPAN',(col,0),(col,5)),
            ('SPAN',(col+1,0),(col+1,5)),
            ('SPAN',(col+2,0),(col+2,5)),
            ('SPAN',(col+3,0),(col+3,5)),
            ('SPAN',(col+4,0),(col+4,5))
        ],
        [45,60, 55,75,45]
        )

def block_common_ar(col):
    return (
        [
            ['Внешний\nосмотр','Проверка\nэлектрической\nпрочности\nизоляции','Потребляемая энергия','','','', '',''],
            ['', '','Опробование (проверка счётного механизма)','','','','','',
             'Проверка\nчувствитель-\nности','','Проверка\nосутствия\nсамохода',''],
            ['','', 'активная энергия','','','реактивная энергия','','', 
             vtext('активная\nэнергия, имп'),vtext('реактивная\nэнергия, имп'), vtext('активная\nэнергия, имп'),vtext('реактивная\nэнергия, имп')],
            ['','', vtext('эталон,\nкВт·ч'),vtext('измерено,\nкВт·ч'),vtext('погреш-\nность,%'),vtext('эталон,\nкВар·ч'),vtext('измерено,\nкВар·ч'),vtext('погреш-\nность,%'), '','', '',''],
            ['','', '','','±1,0','','','±1,0', '≥1','≥1', '≤1','≤1']
        ],
        [
            ('SPAN',(col+2,0),(col+11,0)),

            ('SPAN',(col,0),(col,4)),
            ('SPAN',(col+1,0),(col+1,4)),

            ('SPAN',(col+2,1),(col+7,1)),
            ('SPAN',(col+8,1),(col+9,1)),
            ('SPAN',(col+10,1),(col+11,1)),

            ('SPAN',(col+2,2),(col+4,2)),
            ('SPAN',(col+5,2),(col+7,2)),

            ('SPAN',(col+2,3),(col+2,4)),
            ('SPAN',(col+3,3),(col+3,4)),
            ('SPAN',(col+5,3),(col+5,4)),
            ('SPAN',(col+6,3),(col+6,4)),

            ('SPAN',(col+8,2),(col+8,3)),
            ('SPAN',(col+9,2),(col+9,3)),
            ('SPAN',(col+10,2),(col+10,3)),
            ('SPAN',(col+11,2),(col+11,3)),
        ],
        [45,60, 41,41,30,41,41,30, 30,30, 30,30]
        )


def block_common_arm(col):
    return (
        [
            ['Генерируемая энергия','','','','','', '',''],
            ['Опробование (проверка счётного механизма)','','','','','',
             'Проверка чувствительности',''],
            ['активная энергия','','','реактивная энергия','','', 
             vtext('активная\nэнергия, имп'),vtext('реактивная\nэнергия, имп')],
            [vtext('эталон,\nкВт·ч'),vtext('измерено,\nкВт·ч'),vtext('погреш-\nность, %'),vtext('эталон,\nкВар·ч'),vtext('измерено,\nкВар·ч'),vtext('погреш-\nность, %'), '',''],
            ['','','±1,0','','','±1,0', '≥1','≥1']
        ],
        [
            ('SPAN',(col+0,0),(col+7,0)),

            ('SPAN',(col+0,1),(col+5,1)),
            ('SPAN',(col+6,1),(col+7,1)),

            ('SPAN',(col+0,2),(col+2,2)),
            ('SPAN',(col+3,2),(col+5,2)),

            ('SPAN',(col+0,3),(col+0,4)),
            ('SPAN',(col+1,3),(col+1,4)),
            ('SPAN',(col+3,3),(col+3,4)),
            ('SPAN',(col+4,3),(col+4,4)),

            ('SPAN',(col+6,2),(col+6,3)),
            ('SPAN',(col+7,2),(col+7,3)),
        ],
        [(DATA_W - 180)/4]*2 + [30] + [(DATA_W - 180)/4]*2 + [30, 60,60]
        )



def block_common_a(col):
    return (
        [
            ['Внешний\nосмотр','Проверка\nэлектрической\nпрочности\nизоляции','Активная потребляемая энергия','','', '', ''],
            ['','','','','','',''],
            ['', '','Опробование (проверка счётного механизма)','','',
             'Проверка\nчувствитель-\nности, имп','Проверка\nосутствия\nсамохода, имп'],            
            ['','', vtext('эталон,\nкВт·ч'),vtext('измерено,\nкВт·ч'),vtext('погреш-\nность,%'), '', ''],
            ['','', '','','±1,0','≥1','≤1']
        ],
        [
            ('SPAN',(col+2,0),(col+6,1)),

            ('SPAN',(col,0),(col,4)),
            ('SPAN',(col+1,0),(col+1,4)),

            ('SPAN',(col+2,2),(col+4,2)),

            ('SPAN',(col+5,2),(col+5,3)),
            ('SPAN',(col+6,2),(col+6,3)),
        ],
        [45,60, 82,82,60, 60, 60]
        )


def block_common_am(col):
    return (
        [
            ['Активная генерируемая энергия','','', ''],
            ['','','',''],
            ['Опробование (проверка счётного механизма)','','',
             'Проверка\nчувствитель-\nности, имп'],            
            [vtext('эталон,\nкВт·ч'),vtext('измерено,\nкВт·ч'),vtext('погреш-\nность,%'), ''],
            ['','','±1,0','≥1']
        ],
        [
            ('SPAN',(col+0,0),(col+3,1)),

            ('SPAN',(col+0,2),(col+2,2)),

            ('SPAN',(col+3,2),(col+3,3))
        ],
        [82 + 26,82+26,60+26, 120+27]
        )

def block_clock(col):
    return (
        [
            ['Проверка суточного хода часов', '', ''],
            ['Измеренный период импульсов\nвремени, мкс',
                'Значение суточной коррекции времени,\nустановленное в счетчике, с/сут',
                'Суточный ход часов, с/сут'],
            ['','',''],
            ['','',''],
            ['','',''],
            ['','','±1,0'],
        ],
        [
            ('SPAN',(col,0),(col+2,0)),
            ('SPAN',(col,1),(col,5)),
            ('SPAN',(col+1,1),(col+1,5)),
            ('SPAN',(col+2,1),(col+2,4)),
        ],
        [DATA_W/3]*3
        )

def block_metrology_a(col, phase, direction):
    hdr_ph = 'Определение метрологических характеристик для активной {} энергии ({} канал)'.format(
        {'+':'потребляемой', '-':'генерируемой'}[direction], {'L':'линейный', 'N':'нейтральный'}[phase]) 

    return (
        [
            [hdr_ph,'','',  '','','', '','','', '','',''],
            ['cosϕ = 1','','', 'cosϕ = 0,5и','','', 'cosϕ = 0,8е','','', 'Iмакс','',''],
            ['Ток, % Iϭ','','', '','','', '','','',
                vtext('cosϕ = 1'),vtext('cosϕ = 0,5и'),vtext('cosϕ = 0,8е')],
            ['5','10','100', '10','20','100', '10','20','100', '','',''],
            ['Пределы допустимых погрешностей, %'] + ['']*11,
            ['±1,5','±1,0','±1,0', '±1,5','±1,0','±1,0', '±1,5','±1,0','±1,0', '±1,0','±1,0','±1,0'],
        ],
        [
            ('SPAN',(col,0),(col+11,0)),

            ('SPAN',(col,1),(col+2,1)),
            ('SPAN',(col+3,1),(col+5,1)),
            ('SPAN',(col+6,1),(col+8,1)),
            ('SPAN',(col+9,1),(col+11,1)),

            ('SPAN',(col,2),(col+8,2)),

            ('SPAN',(col+9,2),(col+9,3)),
            ('SPAN',(col+10,2),(col+10,3)),
            ('SPAN',(col+11,2),(col+11,3)),

            ('SPAN',(col,4),(col+11,4)),
        ],
        [DATA_W/12]*12
        )

def block_metrology_r(col, phase, direction):
    hdr_ph = 'Определение метрологических характеристик для реактивной {} энергии ({} канал)'.format(
        {'+':'потребляемой', '-':'генерируемой'}[direction], {'L':'линейный', 'N':'нейтральный'}[phase])

    return (
        [
            [hdr_ph,'','',  '','','', '','','', '','',''],
            ['sinϕ = 1','','', 'sinϕ = 0,5и','','', 'sinϕ = 0,8е','','', 'Iмакс','',''],
            ['Ток, % Iϭ','','', '','','', '','','',
                vtext('sinϕ = 1'),vtext('sinϕ = 0,5и'),vtext('sinϕ = 0,8е')],
            ['5','10','100', '10','20','100', '10','20','100', '','',''],
            ['Пределы допустимых погрешностей, %'] + ['']*11,
            ['±1,5','±1,0','±1,0', '±1,5','±1,0','±1,0', '±1,5','±1,0','±1,0', '±1,0','±1,0','±1,0'],
        ],
        [
            ('SPAN',(col,0),(col+11,0)),

            ('SPAN',(col,1),(col+2,1)),
            ('SPAN',(col+3,1),(col+5,1)),
            ('SPAN',(col+6,1),(col+8,1)),
            ('SPAN',(col+9,1),(col+11,1)),

            ('SPAN',(col,2),(col+8,2)),

            ('SPAN',(col+9,2),(col+9,3)),
            ('SPAN',(col+10,2),(col+10,3)),
            ('SPAN',(col+11,2),(col+11,3)),

            ('SPAN',(col,4),(col+11,4)),
        ],
        [DATA_W/12]*12
        )
'''
def block_metrology_r(col, phase, direction):
    hdr_ph = 'Определение метрологических характеристик для реактивной {} энергии ({} канал)'.format(
        {'+':'потребляемой', '-':'генерируемой'}[direction], {'L':'линейный', 'N':'нейтральный'}[phase])
    return (
        [
            [hdr_ph, '','',  '','','', '','', '','',''],
            ['sinϕ = 1','','','sinϕ = 0,5и','','','sinϕ = 0,25и','','Iмакс','',''],
            ['Ток, % Iϭ','','','','','','','',
                vtext('sinϕ = 1'),vtext('sinϕ = 0,5и'),vtext('sinϕ = 0,25и')],
            ['5','10','100','10','20','100','20','100','','',''],
            ['Пределы допустимых погрешностей, %'] + ['']*10,
            ['±1,5','±1,0','±1,0','±1,5','±1,0','±1,0','±1,5','±1,5','±1,0','±1,0','±1,5'],
        ],
        [
            ('SPAN',(col,0),(col+10,0)),

            ('SPAN',(col,1),(col+2,1)),
            ('SPAN',(col+3,1),(col+5,1)),
            ('SPAN',(col+6,1),(col+7,1)),
            ('SPAN',(col+8,1),(col+10,1)),

            ('SPAN',(col,2),(col+7,2)),

            ('SPAN',(col+8,2),(col+8,3)),
            ('SPAN',(col+9,2),(col+9,3)),
            ('SPAN',(col+10,2),(col+10,3)),

            ('SPAN',(col,4),(col+10,4)),
        ],
        [DATA_W/11]*11
        )
'''
def add_block(res, block, **param):
    b,s,w = res
    b1,s1,w1 = block(len(w), **param)
    for i in range(len(b)):
        b[i].extend(b1[i])
    s.extend(s1)
    w.extend(w1)





    
def tnpa_2948_2020_com(data):
    res = base_block()
    add_block(res, block_common)
    add_block(res, block_clock)

    header, style, width = res
    n = 0
    for mac, place, m in data:
        n += 1
        row = [str(n), str(place), str(mac)]

        #общее
        row.append('годен')
        row.append('годен')
        row.append('годен')
        row.append('годен')
        row.append('годен')

        #время
        val = m.get('- T T')
        row.append('{}'.format(int(val['value']*1000000)) if val is not None else '')
        val = m.get('- Td dTcfg')
        row.append('{:.1f}'.format(val['value']) if val is not None else '')
        val = m.get('- Td dT')
        row.append('{:.1f}'.format(val['value']) if val is not None else '')
        
        header.append(row)

    return base_report.data_table(header, width, style, repeatRows=5)



def tnpa_2948_2020_com_ar(data):
    res = base_block5()
    add_block(res, block_common_ar)

    header, style, width = res
    n = 0
    for mac, place, m in data:
        n += 1
        row = [str(n), str(place), str(mac)]

        #общее
        row.append('годен')
        row.append('годен')

        val = m.get('L A Ub-I15-A45-1')
        if val is not None:
            row.append('{:.5f}'.format(val['etalon']))
            row.append('{:.5f}'.format(val['value']))            
            row.append('{:.2f}'.format(val['error']))
        else:
            row.append('')
            row.append('')
            row.append('')
        val = m.get('L R Ub-I15-A45-1')
        if val is not None:
            row.append('{:.5f}'.format(val['etalon']))
            row.append('{:.5f}'.format(val['value']))            
            row.append('{:.2f}'.format(val['error']))
        else:
            row.append('')
            row.append('')
            row.append('')

        val = m.get('L Ap Ub-Istart')
        row.append('{}'.format(int(val['value'])) if val is not None else '')
        val = m.get('L Rp Ub-Istart-Rl')
        row.append('{}'.format(int(val['value'])) if val is not None else '')
        val = m.get('L Ap U1.15b-Ioff-Toff')
        row.append('{}'.format(int(val['value'])) if val is not None else '')
        val = m.get('L Rp U1.15b-Ioff-Toff')
        row.append('{}'.format(int(val['value'])) if val is not None else '')
        header.append(row)

    return base_report.data_table(header, width, style, repeatRows=5)


def tnpa_2948_2020_com_arm(data):
    res = base_block5()
    add_block(res, block_common_arm)

    header, style, width = res
    n = 0
    for mac, place, m in data:
        n += 1
        row = [str(n), str(place), str(mac)]

        #общее

        val = m.get('L A- Ub-I15-A45-1')
        if val is not None:
            row.append('{:.5f}'.format(val['etalon']))
            row.append('{:.5f}'.format(val['value']))            
            row.append('{:.2f}'.format(val['error']))
        else:
            row.append('')
            row.append('')
            row.append('')
        val = m.get('L R- Ub-I15-A45-1')
        if val is not None:
            row.append('{:.5f}'.format(val['etalon']))
            row.append('{:.5f}'.format(val['value']))            
            row.append('{:.2f}'.format(val['error']))
        else:
            row.append('')
            row.append('')
            row.append('')

        val = m.get('L A-p Ub-Istart')
        row.append('{}'.format(int(val['value'])) if val is not None else '')
        val = m.get('L R-p Ub-Istart-Rl')
        row.append('{}'.format(int(val['value'])) if val is not None else '')

        header.append(row)

    return base_report.data_table(header, width, style, repeatRows=5)



def tnpa_2948_2020_com_a(data):
    res = base_block5()
    add_block(res, block_common_a)

    header, style, width = res
    n = 0
    for mac, place, m in data:
        n += 1
        row = [str(n), str(place), str(mac)]

        #общее
        row.append('годен')
        row.append('годен')

        val = m.get('L A Ub-I15-A45-1')
        if val is not None:
            row.append('{:.5f}'.format(val['etalon']))
            row.append('{:.5f}'.format(val['value']))            
            row.append('{:.2f}'.format(val['error']))
        else:
            row.append('')
            row.append('')
            row.append('')

        val = m.get('L Ap Ub-Istart')
        row.append('{}'.format(int(val['value'])) if val is not None else '')
        val = m.get('L Ap U1.15b-Ioff-Toff')
        row.append('{}'.format(int(val['value'])) if val is not None else '')
        header.append(row)

    return base_report.data_table(header, width, style, repeatRows=5)


def tnpa_2948_2020_com_am(data):
    res = base_block5()
    add_block(res, block_common_am)

    header, style, width = res
    n = 0
    for mac, place, m in data:
        n += 1
        row = [str(n), str(place), str(mac)]

        #общее

        val = m.get('L A- Ub-I15-A45-1')
        if val is not None:
            row.append('{:.5f}'.format(val['etalon']))
            row.append('{:.5f}'.format(val['value']))            
            row.append('{:.2f}'.format(val['error']))
        else:
            row.append('')
            row.append('')
            row.append('')

        val = m.get('L Ap- Ub-Istart')
        row.append('{}'.format(int(val['value'])) if val is not None else '')

        header.append(row)

    return base_report.data_table(header, width, style, repeatRows=5)

def tnpa_2948_2020_A(data, phase, direction):
    res = base_block()
    add_block(res, block_metrology_a, phase=phase, direction = direction)

    header, style, width = res
    n = 0
    for mac, place, m in data:
        n += 1
        row = [str(n), str(place), str(mac)]
        #метрология
        gr = {'+':'A', '-':'A-'}[direction]
        for id in ['Ub-I0.05b','Ub-I0.1b','Ub-Ib', 
                   'Ub-I0.1b-R0.5l','Ub-I0.2b-R0.5l','Ub-Ib-R0.5l', 
                   'Ub-I0.1b-R0.8c','Ub-I0.2b-R0.8c','Ub-Ib-R0.8c', 
                   'Ub-Imax','Ub-Imax-R0.5l','Ub-Imax-R0.8c']:

            val = m.get(phase + ' ' + gr + ' ' + id, None)
            if val != None:
                row.append('{:.2f}'.format(val['error']))
                
        header.append(row)

    return base_report.data_table(header, width, style, repeatRows=6)

def tnpa_2948_2020_R(data, phase, direction):
    res = base_block()
    add_block(res, block_metrology_r, phase=phase, direction = direction)

    header, style, width = res
    n = 0
    for mac, place, m in data:
        n += 1
        row = [str(n), str(place), str(mac)]
        #метрология
        gr = {'+':'R', '-':'R-'}[direction]
        for id in ['Ub-I0.05b-Rl','Ub-I0.1b-Rl','Ub-Ib-Rl', 
                   'Ub-I0.1b-R0.5l','Ub-I0.2b-R0.5l','Ub-Ib-R0.5l', 
                   'Ub-I0.1b-R0.8c','Ub-I0.2b-R0.8c','Ub-Ib-R0.8c',
                   'Ub-Imax-Rl','Ub-Imax-R0.5l','Ub-Imax-R0.8c']:

            val = m.get(phase + ' ' + gr + ' ' + id, None)
            if val != None:
                row.append('{:.2f}'.format(val['error']))
        header.append(row)

    return base_report.data_table(header, width, style, repeatRows=6)

def tnpa_2948_2020_clock(data):
    res = base_block()
    add_block(res, block_clock)

    header, style, width = res
    n = 0
    for mac, place, m in data:
        n += 1
        row = [str(n), str(place), str(mac)]

        #время
        val = m.get('- T T')
        row.append('{}'.format(int(val['value']*1000000)) if val is not None else '')
        val = m.get('- Td dTcfg')
        row.append('{:.1f}'.format(val['value']) if val is not None else '')
        val = m.get('- Td dT')
        row.append('{:.1f}'.format(val['value']) if val is not None else '')
        
        header.append(row)

    return base_report.data_table(header, width, style, repeatRows=6)


def tnpa_2948_2020_extra(data):
    res = extra_block()
    header, style, width = res
    n = 0
    for mac, place, m in data:
        n += 1
        row = [str(n), str(place), str(mac), '']
        header.append(row)
    return base_report.data_table(header, width, style, repeatRows=1)




#--------------

class tnpa_2948_2020(base_report.Report):
    algoritm = tnpa_list.keys()

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, pageNumbers = True,
                                footer = '№ {}-СЭТ/{}'.format(kwargs['info']['id'],kwargs['info']['time'].year),
                                **kwargs)
    
    def addProtocol(self, number, model, customer, lab_name, lab_descr, place, date, unit, t, f, p):
        self.add_protocol()

        self.tnpa = tnpa_list[model]
        self.elements.extend([
            base_report.page_header(number, self.tnpa['model']),
            base_report.org_info(customer, lab_descr, place),
            base_report.report_info(date, self.tnpa['name']),
            base_report.unit_info(unit),
            base_report.measure_info(t, f, p),
            base_report.add_text('Результаты поверки:'),
            ])

    def endProtocol(self, fio):
        #self.elements.append(tnpa_2948_2020_com(self.devs))
        #self.tnpa['R'] = False

        if self.tnpa['R']:
            self.elements.append(tnpa_2948_2020_com_ar(self.devs))
        else:
            self.elements.append(tnpa_2948_2020_com_a(self.devs))

        if self.tnpa['gen']:
            if self.tnpa['R']:
                self.elements.append(tnpa_2948_2020_com_arm(self.devs))
            else:
                self.elements.append(tnpa_2948_2020_com_am(self.devs))
        
        
        self.elements.append(tnpa_2948_2020_A(self.devs, 'L', '+'))
        
        if self.tnpa['gen']:
            self.elements.append(base_report.add_text(''))
            self.elements.append(tnpa_2948_2020_A(self.devs, 'L', '-'))

        if self.tnpa['R']:
            self.elements.append(base_report.add_text(''))
            self.elements.append(tnpa_2948_2020_R(self.devs, 'L', '+'))
            if self.tnpa['gen']:
                self.elements.append(base_report.add_text(''))
                self.elements.append(tnpa_2948_2020_R(self.devs, 'L', '-'))

        if self.tnpa['N']:
            self.elements.append(base_report.add_text(''))
            self.elements.append(tnpa_2948_2020_A(self.devs, 'N', '+'))
            if self.tnpa['gen']:
                self.elements.append(base_report.add_text(''))
                self.elements.append(tnpa_2948_2020_A(self.devs, 'N', '-'))

            if self.tnpa['R']:
                self.elements.append(base_report.add_text(''))
                self.elements.append(tnpa_2948_2020_R(self.devs, 'N', '+'))
                if self.tnpa['gen']:
                    self.elements.append(base_report.add_text(''))
                    self.elements.append(tnpa_2948_2020_R(self.devs, 'N', '-'))

        self.elements.append(tnpa_2948_2020_clock(self.devs))
        self.elements.append(base_report.add_text('Дополнительные сведения'))
        self.elements.append(tnpa_2948_2020_extra(self.devs))

        self.elements.append(base_report.signature(fio))