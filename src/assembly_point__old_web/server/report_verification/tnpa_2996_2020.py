import reportlab.lib.colors as colors
from report_verification.vtext import vtext
import report_verification.base_report as base_report

MAC_W = 86.0
PAGE_W = 535.0
DATA_W = PAGE_W - MAC_W

tnpa_list = {
    'SM302 5-60 AR':{'model':'SM302 5(60)А. 1/1. D.R.P.O.2RF.2RS.VR.L', 'name':'МРБ МП.2996-2020', 'R':True, 'gen':True, 'mod':0},
    'SM302 5-100 AR':{'model':'SM302 5(100)А. 1/1. D.R.P.O.2RF.2RS.VR.L', 'name':'МРБ МП.2996-2020', 'R':True, 'gen':True, 'mod':0},
    'SM302 K 5-10 AR':{'model':'SM302 5(10)А. 1/1. D.P.O.2RF.2RS.VR.L', 'name':'МРБ МП.2996-2020', 'R':True, 'gen':True, 'mod':1},
    'SM302 K0.5 5-10 AR':{'model':'SM302 5(10)А. 0,5S/0,5. D.P.O.2RF.2RS.VR.L', 'name':'МРБ МП.2996-2020', 'R':True, 'gen':True, 'mod':2},
}

def base_block():
    return (
        [
            [vtext('№ п/п'), vtext('№ места'), vtext('№ счетчика')],
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
            ('SPAN',(0,0),(0,4)),
            ('SPAN',(1,0),(1,4)),
            ('SPAN',(2,0),(2,4)),
        ],
        [18,18,50]      
        )

def base_block6():
    return (
        [
            [vtext('№ п/п'), vtext('№ места'), vtext('№ счетчика')],
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

def extra_block():
    return (
        [
            [vtext('№ п/п'), vtext('№ места'), vtext('№ счетчика'),'№ клейма-наклейки'],
        ],
        [
            ('FONT', (0, 0), (-1, -1), 'Times New Roman', 8),
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('BACKGROUND',(0,0),(1,1),colors.white),
        ],
        [18,18,50] + [DATA_W]
        )

def block_common_ar(col, mod):
    return (
        [
            ['Внешний\nосмотр','Проверка\nэлектрической\nпрочности\nизоляции','Потребляемая энергия','','','', '',''],
            ['', '','Опробование (проверка счётного механизма)','','','','','',
             'Проверка\nчувствитель-\nности','','Проверка\nосутствия\nсамохода',''],
            ['','', 'активная энергия','','','реактивная энергия','','', 
             vtext('активная\nэнергия, имп'),vtext('реактивная\nэнергия, имп'), vtext('активная\nэнергия, имп'),vtext('реактивная\nэнергия, имп')],
            ['','', vtext('эталон,\nкВт·ч'),vtext('измерено,\nкВт·ч'),vtext('погреш-\nность,%'),vtext('эталон,\nкВар·ч'),vtext('измерено,\nкВар·ч'),vtext('погреш-\nность,%'), '','', '',''],
            ['','', '','','±1,0' if mod!=2 else '±0,5' ,'','','±1,0' if mod!=2 else '±0,5', '≥1','≥1', '≤1','≤1']
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


def block_common_arm(col, mod):
    return (
        [
            ['Генерируемая энергия','','','','','', '',''],
            ['Опробование (проверка счётного механизма)','','','','','',
             'Проверка чувствительности',''],
            ['активная энергия','','','реактивная энергия','','', 
             vtext('активная\nэнергия, имп'),vtext('реактивная\nэнергия, имп')],
            [vtext('эталон,\nкВт·ч'),vtext('измерено,\nкВт·ч'),vtext('погреш-\nность, %'),vtext('эталон,\nкВар·ч'),vtext('измерено,\nкВар·ч'),vtext('погреш-\nность, %'), '',''],
            ['','','±1,0' if mod!=2 else '±0,5','','','±1,0' if mod!=2 else '±0,5', '≥1','≥1']
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

def block_clock(col):
    return (
        [
            ['Проверка суточного хода часов', '', ''],
            ['Измеренный период импульсов\nвремени, мкс',
                'Значение суточной коррекции времени,\nустановленное в счетчике, с/сут',
                'Суточный ход часов, с/сут'],
            ['','',''],
            ['','',''],
            ['','','±1,0'],
        ],
        [
            ('SPAN',(col,0),(col+2,0)),
            ('SPAN',(col,1),(col,4)),
            ('SPAN',(col+1,1),(col+1,4)),
            ('SPAN',(col+2,1),(col+2,3))
        ],
        [DATA_W / 3] * 3
        )










def block_metrology_a(col, direction, mod):
    hdr_ph = 'Определение метрологических характеристик для активной {} энергии при симметричной нагрузке'.format(
        {'+':'потребляемой', '-':'генерируемой'}[direction]
        ) 

    return (
        [
            [hdr_ph,'','',  '','','', '','','', '','',''],
            ['cosϕ = 1','','', 'cosϕ = 0,5и','','', 'cosϕ = 0,8е','','', 'Iмакс','',''],
            ['Ток, % '+('Iϭ','Iном','Iном')[mod],'','', '','','', '','','',
                vtext('cosϕ = 1'),vtext('cosϕ = 0,5и'),vtext('cosϕ = 0,8е')],
            (['5','10','100', '10','20','100', '10','20','100', '','',''],#1%
             ['2','5','100', '5','10','100', '5','10','100', '','',''],#1% ПКВ
             ['1','5','100', '2','10','100', '2','10','100', '','','']#0,5% ПКВ
             )[mod],
             ['Пределы допустимых погрешностей, %'] + ['']*11,
            (['±1,5','±1,0','±1,0', '±1,5','±1,0','±1,0', '±1,5','±1,0','±1,0', '±1,0','±1,0','±1,0'],#1%
             ['±1,5','±1,0','±1,0', '±1,5','±1,0','±1,0', '±1,5','±1,0','±1,0', '±1,0','±1,0','±1,0'],#1% ПКВ
             ['±1,0','±0,5','±0,5', '±1,0','±0,6','±0,6', '±1,0','±0,6','±0,6', '±0,5','±0,6','±0,6']#0,5% ПКВ
             )[mod]
        ],
        [
            ('SPAN',(col,0),(col+11,0)),

            ('SPAN',(col,1),(col+2,1)),
            ('SPAN',(col+3,1),(col+5,1)),
            ('SPAN',(col+6,1),(col+8,1)),
            ('SPAN',(col+9,1),(col+11,1)),

            ('SPAN',(col,2),(col+8,2)),

            ('SPAN',(col,4),(col+11,4)),

            ('SPAN',(col+9,2),(col+9,3)),
            ('SPAN',(col+10,2),(col+10,3)),
            ('SPAN',(col+11,2),(col+11,3))
        ],
        [DATA_W / 12]*12
        )

def block_metrology_r(col, direction, mod):
    hdr_ph = 'Определение метрологических характеристик для реактивной {} энергии при симметричной нагрузке'.format(
        {'+':'потребляемой', '-':'генерируемой'}[direction]
        )
    return (
        [
            [hdr_ph, '','',  '','','', '','', '','',''],
            ['sinϕ = 1','','','sinϕ = 0,5и','','','sinϕ = 0,8е','','Iмакс','',''],
            ['Ток, % '+('Iϭ','Iном')[mod],'','','','','','','',
                vtext('sinϕ = 1'),vtext('sinϕ = 0,5и'),vtext('sinϕ = 0,8е')],
            (['5','10','100','10','20','100','20','100','','',''],#1%
             ['2','5','100','5','10','100','10','100','','','']#1% ПКВ
             )[mod],
            ['Пределы допустимых погрешностей, %'] + ['']*10,
            ['±1,5','±1,0','±1,0','±1,5','±1,0','±1,0','±1,0','±1,0','±1,0','±1,0','±1,0'],
        ],
        [
            ('SPAN',(col,0),(col+10,0)),

            ('SPAN',(col,1),(col+2,1)),
            ('SPAN',(col+3,1),(col+5,1)),
            ('SPAN',(col+6,1),(col+7,1)),
            ('SPAN',(col+8,1),(col+10,1)),

            ('SPAN',(col,2),(col+7,2)),

            ('SPAN',(col,4),(col+10,4)),

            ('SPAN',(col+8,2),(col+8,3)),
            ('SPAN',(col+9,2),(col+9,3)),
            ('SPAN',(col+10,2),(col+10,3))
        ],
        [DATA_W / 11]*11
        )

def block_metrology_rk05(col, direction, mod):
    hdr_ph = 'Определение метрологических характеристик для реактивной {} энергии при симметричной нагрузке'.format(
        {'+':'потребляемой', '-':'генерируемой'}[direction]
        )
    return (
        [
            [hdr_ph, '','',  '','','',  '',''],
            ['sinϕ = 1','','','sinϕ = 0,5и','','','Iмакс',''],
            ['Ток, % Iном','','','','','',
                vtext('sinϕ = 1'),vtext('sinϕ = 0,5и')],
            ['1','5','100','2','10','100','',''],
            ['Пределы допустимых погрешностей, %'] + ['']*7,
            ['±1,0','±0,5','±0,5','±1,0','±0,6','±0,6','±0,5','±0,6'],
        ],
        [
            ('SPAN',(col,0),(col+7,0)),

            ('SPAN',(col,1),(col+2,1)),
            ('SPAN',(col+3,1),(col+5,1)),
            ('SPAN',(col+6,1),(col+7,1)),

            ('SPAN',(col,2),(col+5,2)),

            ('SPAN',(col,4),(col+7,4)),

            ('SPAN',(col+6,2),(col+6,3)),
            ('SPAN',(col+7,2),(col+7,3))
        ],
        [DATA_W / 8]*8
        )










def block_metrology_p_a(col, phase, mod):
    hdr_ph = 'Определение метрологических характеристик для активной потребляемой энергии по фазе {}'.format(
        phase)
    return (
        [
            [hdr_ph, '', '', '', '', '', ''],
            ['cosϕ = 1','','cosϕ = 0,5и','','Iмакс','', 'Разность\nс симметричной\nпри {}, cosϕ = 1'.format(('Iϭ','Iном','Iном')[mod])],
            ['Ток, % '+('Iϭ','Iном','Iном')[mod],'','','',
                vtext('cosϕ = 1'),vtext('cosϕ = 0,5и'),''],
            (['10','100','20','100','','',''],#1%
             ['5','100','10','100','','',''],#1% ПКВ
             ['5','100','10','100','','','']#0,5% ПКВ
             )[mod],
             ['Пределы допустимых погрешностей, %'] + ['']*6,
            (['±2,0','±2,0','±2,0','±2,0','±2,0','±2,0','±1,5'],#1%
             ['±2,0','±2,0','±2,0','±2,0','±2,0','±2,0','±1,5'],#1% ПКВ
             ['±0,6','±0,6','±1,0','±1,0','±0,6','±1,0','±1,0']#0,5% ПКВ
             )[mod],
        ],
        [
            ('SPAN',(col,0),(col+6,0)),

            ('SPAN',(col,1),(col+1,1)),
            ('SPAN',(col+2,1),(col+3,1)),
            ('SPAN',(col+4,1),(col+5,1)),

            ('SPAN',(col,2),(col+3,2)),

            ('SPAN',(col,4),(col+6,4)),

            ('SPAN',(col+4,2),(col+4,3)),
            ('SPAN',(col+5,2),(col+5,3)),

            ('SPAN',(col+6,1),(col+6,3)),
        ],
        [(DATA_W - 80) / 6]*6 + [80]
        )

def block_metrology_p_am(col, phase, mod):
    hdr_ph = 'Определение метрологических характеристик для активной генерируемой энергии по фазе {}'.format(
        phase)
    return (
        [
            [hdr_ph, '', '', '', '', ''],
            ['cosϕ = 1','','cosϕ = 0,5и','','Iмакс',''],
            ['Ток, % '+('Iϭ','Iном','Iном')[mod],'','','',
                vtext('cosϕ = 1'),vtext('cosϕ = 0,5и')],
            (['10','100','20','100','',''],#1%
             ['5','100','10','100','',''],#1% ПКВ
             ['5','100','10','100','','']#0,5% ПКВ
             )[mod],
             ['Пределы допустимых погрешностей, %'] + ['']*5,
            (['±2,0','±2,0','±2,0','±2,0','±2,0','±2,0'],#1%
             ['±2,0','±2,0','±2,0','±2,0','±2,0','±2,0'],#1% ПКВ
             ['±0,6','±0,6','±1,0','±1,0','±0,6','±1,0']#0,5% ПКВ
             )[mod],
        ],
        [
            ('SPAN',(col,0),(col+5,0)),

            ('SPAN',(col,1),(col+1,1)),
            ('SPAN',(col+2,1),(col+3,1)),
            ('SPAN',(col+4,1),(col+5,1)),

            ('SPAN',(col,2),(col+3,2)),

            ('SPAN',(col,4),(col+5,4)),

            ('SPAN',(col+4,2),(col+4,3)),
            ('SPAN',(col+5,2),(col+5,3)),
        ],
        [DATA_W / 6]*6
        )

def block_metrology_p_r(col, phase, mod):
    hdr_ph = 'Определение метрологических характеристик для реактивной потребляемой энергии по фазе {}'.format( 
        phase)
    return (
        [
            [hdr_ph, '', '', '', '', '', ''],
            ['sinϕ = 1','','sinϕ = 0,5и','','Iмакс','', 'Разность\nс симметричной\nпри {}, sinϕ = 1'.format(('Iϭ','Iном','Iном')[mod])],
            ['Ток, % '+('Iϭ','Iном','Iном')[mod],'','','',
                vtext('sinϕ = 1'),vtext('sinϕ = 0,5и'), ''],
            (['10','100','20','100','','',''],#1%
             ['5','100','10','100','','',''],#1% ПКВ
             ['5','100','10','100','','','']#0,5% ПКВ
             )[mod],
             ['Пределы допустимых погрешностей, %'] + ['']*6,
            (['±1,5','±1,5','±1,5','±1,5','±1,5','±1,5', '±2,5'],#1%
             ['±1,5','±1,5','±1,5','±1,5','±1,5','±1,5', '±2,5'],#1% ПКВ
             ['±0,6','±0,6','±1,0','±1,0','±0,6','±1,0', '±1,5']#0,5% ПКВ
             )[mod],
        ],
        [
            ('SPAN',(col,0),(col+6,0)),

            ('SPAN',(col,1),(col+1,1)),
            ('SPAN',(col+2,1),(col+3,1)),
            ('SPAN',(col+4,1),(col+5,1)),

            ('SPAN',(col,2),(col+3,2)),

            ('SPAN',(col,4),(col+6,4)),

            ('SPAN',(col+4,2),(col+4,3)),
            ('SPAN',(col+5,2),(col+5,3)),

            ('SPAN',(col+6,1),(col+6,3)),
        ],
        [(DATA_W - 80) / 6]*6 + [80]        
        )

def block_metrology_p_rm(col, phase, mod):
    hdr_ph = 'Определение метрологических характеристик для реактивной генерируемой энергии по фазе {}'.format(
        phase)
    return (
        [
            [hdr_ph, '', '', '', '', ''],
            ['sinϕ = 1','','sinϕ = 0,5и','','Iмакс',''],
            ['Ток, % '+('Iϭ','Iном','Iном')[mod],'','','',
                vtext('sinϕ = 1'),vtext('sinϕ = 0,5и')],
            (['10','100','20','100','',''],#1%
             ['5','100','10','100','',''],#1% ПКВ
             ['5','100','10','100','','']#0,5% ПКВ
             )[mod],
             ['Пределы допустимых погрешностей, %'] + ['']*5,
            (['±1,5','±1,5','±1,5','±1,5','±1,5','±1,5'],#1%
             ['±1,5','±1,5','±1,5','±1,5','±1,5','±1,5'],#1% ПКВ
             ['±0,6','±0,6','±1,0','±1,0','±0,6','±1,0']#0,5% ПКВ
             )[mod],
        ],
        [
            ('SPAN',(col,0),(col+5,0)),

            ('SPAN',(col,1),(col+1,1)),
            ('SPAN',(col+2,1),(col+3,1)),
            ('SPAN',(col+4,1),(col+5,1)),

            ('SPAN',(col,2),(col+3,2)),

            ('SPAN',(col,4),(col+5,4)),

            ('SPAN',(col+4,2),(col+4,3)),
            ('SPAN',(col+5,2),(col+5,3)),
        ],
        [DATA_W / 6]*6
        )

def block_metrology_p_ui(col, phase, mod):
    hdr_ph = 'Определение метрологических характеристик для тока и напряжения по фазе {}'.format(
        phase)
    return (
        [
            [hdr_ph, '', '', '', '', ''],
            ['Напряжение при '+('Iϭ','Iном','Iном')[mod],'','','Ток при Uном','',''],
            ['Напряжение, % Uном','','', 'Ток, % '+('Iϭ','Iном','Iном')[mod],'','Imax'],
            ['80','100','115','1' if mod==2 else '5','100',''],
            ['Пределы допустимых погрешностей, %'] + ['']*5,
            ['±1,0','±1,0','±1,0','±1,0','±1,0','±1,0'],
        ],
        [
            ('SPAN',(col,0),(col+5,0)),

            ('SPAN',(col,1),(col+2,1)),
            ('SPAN',(col+3,1),(col+5,1)),

            ('SPAN',(col,2),(col+2,2)),
            ('SPAN',(col+3,2),(col+4,2)),

            ('SPAN',(col,4),(col+5,4)),

            ('SPAN',(col+5,2),(col+5,3)),
        ],
        [DATA_W / 6]*6
        )

def add_block(res, block, **param):
    b,s,w = res
    b1,s1,w1 = block(len(w), **param)
    for i in range(len(b)):
        b[i].extend(b1[i])
    s.extend(s1)
    w.extend(w1)





    
def tnpa_2996_2020_com_ar(mod, data):
    res = base_block()
    add_block(res, block_common_ar, mod = mod)

    header, style, width = res
    n = 0
    for mac, place, m in data:
        n += 1
        row = [str(n), str(place), str(mac)]

        #общее
        row.append('годен')
        row.append('годен')

        val = m.get('S A Ub-I40-A45-1' if mod==0 else 'S A Ub-I10-A45-1')
        if val is not None:
            row.append('{:.5f}'.format(val['etalon']))
            row.append('{:.5f}'.format(val['value']))            
            row.append('{:.2f}'.format(val['error']))
        else:
            row.append('')
            row.append('')
            row.append('')
        val = m.get('S R Ub-I40-A45-1' if mod==0 else 'S R Ub-I10-A45-1')
        if val is not None:
            row.append('{:.5f}'.format(val['etalon']))
            row.append('{:.5f}'.format(val['value']))            
            row.append('{:.2f}'.format(val['error']))
        else:
            row.append('')
            row.append('')
            row.append('')

        val = m.get('S Ap Ub-Istart')
        row.append('{}'.format(int(val['value'])) if val is not None else '')
        val = m.get('S Rp Ub-Istart')
        row.append('{}'.format(int(val['value'])) if val is not None else '')
        val = m.get('S Ap U1.15b-Ioff-Toff')
        row.append('{}'.format(int(val['value'])) if val is not None else '')
        val = m.get('S Rp U1.15b-Ioff-Toff')
        row.append('{}'.format(int(val['value'])) if val is not None else '')
        header.append(row)

    return base_report.data_table(header, width, style, repeatRows=5)


def tnpa_2996_2020_com_arm(mod, data):
    res = base_block()
    add_block(res, block_common_arm, mod = mod)

    header, style, width = res
    n = 0
    for mac, place, m in data:
        n += 1
        row = [str(n), str(place), str(mac)]

        #общее

        val = m.get('S A- Ub-I40-A45-1' if mod==0 else 'S A- Ub-I10-A45-1')
        if val is not None:
            row.append('{:.5f}'.format(val['etalon']))
            row.append('{:.5f}'.format(val['value']))            
            row.append('{:.2f}'.format(val['error']))
        else:
            row.append('')
            row.append('')
            row.append('')
        val = m.get('S R- Ub-I40-A45-1' if mod==0 else 'S R- Ub-I10-A45-1')
        if val is not None:
            row.append('{:.5f}'.format(val['etalon']))
            row.append('{:.5f}'.format(val['value']))            
            row.append('{:.2f}'.format(val['error']))
        else:
            row.append('')
            row.append('')
            row.append('')

        val = m.get('S Ap- Ub-Istart')
        row.append('{}'.format(int(val['value'])) if val is not None else '')
        val = m.get('S Rp- Ub-Istart')
        row.append('{}'.format(int(val['value'])) if val is not None else '')

        header.append(row)

    return base_report.data_table(header, width, style, repeatRows=5)

def tnpa_2996_2020_a(mod, data, direction):
    res = base_block6()
    add_block(res, block_metrology_a, mod=mod, direction = direction)

    header, style, width = res
    n = 0
    for mac, place, m in data:
        n += 1
        row = [str(n), str(place), str(mac)]
        #метрология
        gr = {'+':'A', '-':'A-'}[direction]
        msrs = (
            # Прямой
            ('Ub-I0.05b','Ub-I0.1b','Ub-Ib',                    'Ub-I0.1b-R0.5l','Ub-I0.2b-R0.5l','Ub-Ib-R0.5l', 
             'Ub-I0.1b-R0.8c','Ub-I0.2b-R0.8c','Ub-Ib-R0.8c',   'Ub-Imax','Ub-Imax-R0.5l','Ub-Imax-R0.8c'),
            # ПКВ 1
            ('Ub-I0.02b','Ub-I0.05b','Ub-Ib',                   'Ub-I0.05b-R0.5l','Ub-I0.1b-R0.5l','Ub-Ib-R0.5l',
             'Ub-I0.05b-R0.8c','Ub-I0.1b-R0.8c','Ub-Ib-R0.8c',  'Ub-Imax','Ub-Imax-R0.5l','Ub-Imax-R0.8c'),
            # ПКВ 0,5
            ('Ub-I0.01b','Ub-I0.05b','Ub-Ib',                   'Ub-I0.02b-R0.5l','Ub-I0.1b-R0.5l','Ub-Ib-R0.5l',
             'Ub-I0.02b-R0.8c','Ub-I0.1b-R0.8c','Ub-Ib-R0.8c',  'Ub-Imax','Ub-Imax-R0.5l','Ub-Imax-R0.8c')
            )[mod]

        for id in msrs:

            val = m.get('S' + ' ' + gr + ' ' + id, None)
            if val != None:
                row.append('{:.2f}'.format(val['error']))
            else:
                row.append('')                
        header.append(row)

    return base_report.data_table(header, width, style, repeatRows=6)

def tnpa_2996_2020_r(mod, data, direction):
    res = base_block6()
    add_block(res, block_metrology_rk05 if mod==2 else block_metrology_r, mod=mod, direction = direction)

    header, style, width = res
    n = 0
    for mac, place, m in data:
        n += 1
        row = [str(n), str(place), str(mac)]

        #метрология
        gr = {'+':'R', '-':'R-'}[direction]
        msrs = (
            # Прямой
            ('Ub-I0.05b-Rl','Ub-I0.1b-Rl','Ub-Ib-Rl',   'Ub-I0.1b-R0.5l','Ub-I0.2b-R0.5l','Ub-Ib-R0.5l', 
             'Ub-I0.2b-R0.8c','Ub-Ib-R0.8c',            'Ub-Imax-Rl','Ub-Imax-R0.5l','Ub-Imax-R0.8c'),
            # ПКВ 1
            ('Ub-I0.02b-Rl','Ub-I0.05b-Rl','Ub-Ib-Rl',   'Ub-I0.05b-R0.5l','Ub-I0.1b-R0.5l','Ub-Ib-R0.5l', 
             'Ub-I0.1b-R0.8c','Ub-Ib-R0.8c',            'Ub-Imax-Rl','Ub-Imax-R0.5l','Ub-Imax-R0.8c'),
            # ПКВ 0,5
            ('Ub-I0.01b-Rl','Ub-I0.05b-Rl','Ub-Ib-Rl',   'Ub-I0.02b-R0.5l','Ub-I0.1b-R0.5l','Ub-Ib-R0.5l', 
                                                        'Ub-Imax-Rl','Ub-Imax-R0.5l')
            )[mod]

        for id in msrs:

            val = m.get('S' + ' ' + gr + ' ' + id, None)
            if val != None:
                row.append('{:.2f}'.format(val['error']))
            else:
                row.append('')
        header.append(row)

    return base_report.data_table(header, width, style, repeatRows=6)

def tnpa_2996_2020_p_a(mod, data, phase, direction):
    res = base_block6()
    add_block(res, block_metrology_p_a if direction=='+' else block_metrology_p_am, mod = mod, phase = phase)

    header, style, width = res
    n = 0
    for mac, place, m in data:
        n += 1
        row = [str(n), str(place), str(mac)]
        #метрология
        gr = {'+':'A', '-':'A-'}[direction]
        msrs = (
            # Прямой
            ('Ub-I0.1b','Ub-Ib','Ub-I0.2b-R0.5l','Ub-Ib-R0.5l','Ub-Imax','Ub-Imax-R0.5l'),
            # ПКВ 1
            ('Ub-I0.05b','Ub-Ib','Ub-I0.1b-R0.5l','Ub-Ib-R0.5l','Ub-Imax','Ub-Imax-R0.5l'),
            # ПКВ 0,5
            ('Ub-I0.05b','Ub-Ib','Ub-I0.1b-R0.5l','Ub-Ib-R0.5l','Ub-Imax','Ub-Imax-R0.5l')
            )[mod]
        for id in msrs:
            val = m.get(phase + ' ' + gr + ' ' + id, None)
            if val != None:
                row.append('{:.2f}'.format(val['error']))
            else:
                row.append('')

        if direction=='+':
            val = m.get(phase + ' dA Ub-Ib', None)
            if val != None:
                row.append('{:.2f}'.format(val['error']))
            else:
                row.append('')
                
        header.append(row)

    return base_report.data_table(header, width, style, repeatRows=6)
'''
def tnpa_2996_2020_p_am(mod, data, phase):
    res = base_block()
    add_block(res, block_metrology_p_am, mod=mod, phase = phase)

    header, style, width = res
    n = 0
    for mac, place, m in data:
        n += 1
        row = [str(place), str(mac)]
        #метрология
        gr = 'A-'
        msrs = (
            # Прямой
            ('Ub-I0.1b','Ub-Ib','Ub-I0.2b-R0.5l','Ub-Ib-R0.5l','Ub-Imax','Ub-Imax-R0.5l'),
            # ПКВ 1
            ('Ub-I0.1b','Ub-Ib','Ub-I0.2b-R0.5l','Ub-Ib-R0.5l','Ub-Imax','Ub-Imax-R0.5l'),
            # ПКВ 0,5
            ('Ub-I0.1b','Ub-Ib','Ub-I0.2b-R0.5l','Ub-Ib-R0.5l','Ub-Imax','Ub-Imax-R0.5l')
            )[mod]
        for id in msrs:

            val = m.get(phase + ' ' + gr + ' ' + id, None)
            if val != None:
                row.append('{:.2f}'.format(val['error']))
            else:
                row.append('')                
        header.append(row)

    return base_report.data_table(header, width, style, repeatRows=5)
'''
def tnpa_2996_2020_p_r(mod, data, phase, direction):
    res = base_block6()
    add_block(res, block_metrology_p_r if direction=='+' else block_metrology_p_rm, mod = mod, phase = phase)

    header, style, width = res
    n = 0
    for mac, place, m in data:
        n += 1
        row = [str(n), str(place), str(mac)]
        #метрология
        gr = {'+':'R', '-':'R-'}[direction]
        msrs = (
            # Прямой
            ('Ub-I0.1b-Rl','Ub-Ib-Rl','Ub-I0.2b-R0.5l','Ub-Ib-R0.5l','Ub-Imax-Rl','Ub-Imax-R0.5l'),
            # ПКВ 1
            ('Ub-I0.05b-Rl','Ub-Ib-Rl','Ub-I0.1b-R0.5l','Ub-Ib-R0.5l','Ub-Imax-Rl','Ub-Imax-R0.5l'),
            # ПКВ 0,5
            ('Ub-I0.05b-Rl','Ub-Ib-Rl','Ub-I0.1b-R0.5l','Ub-Ib-R0.5l','Ub-Imax-Rl','Ub-Imax-R0.5l')
            )[mod]
        for id in msrs:
            val = m.get(phase + ' ' + gr + ' ' + id, None)
            if val != None:
                row.append('{:.2f}'.format(val['error']))
            else:
                row.append('')     
                
        if direction=='+':
            val = m.get(phase + ' dR Ub-Ib-Rl', None)
            if val != None:
                row.append('{:.2f}'.format(val['error']))
            else:
                row.append('')

        header.append(row)

    return base_report.data_table(header, width, style, repeatRows=6)
'''
def tnpa_2996_2020_p_rm(mod, data, phase):
    res = base_block()
    add_block(res, block_metrology_p_rm, phase = phase)

    header, style, width = res
    n = 0
    for mac, place, m in data:
        n += 1
        row = [str(place), str(mac)]
        #метрология
        gr = 'R-'
        for id in ['Ub-I0.1b-Rl','Ub-Ib-Rl','Ub-I0.2b-R0.5l','Ub-Ib-R0.5l','Ub-Imax-Rl','Ub-Imax-R0.5l']:
            val = m.get(phase + ' ' + gr + ' ' + id, None)
            if val != None:
                row.append('{:.2f}'.format(val['error']))
            else:
                row.append('')                
        header.append(row)

    return base_report.data_table(header, width, style, repeatRows=5)
'''

def tnpa_2996_2020_p_ui(mod, data, phase):
    res = base_block6()
    add_block(res, block_metrology_p_ui, mod=mod, phase = phase)

    header, style, width = res
    n = 0
    for mac, place, m in data:
        n += 1
        row = [str(n), str(place), str(mac)]
        #метрология
        for id in ['U U0.8b-Ib','U Ub-Ib','U U1.15b-Ib','I Ub-0.01Ib' if mod==2 else 'I Ub-0.05Ib','I Ub-Ib','I Ub-Imax']:
            val = m.get(phase + ' ' + id, None)
            if val != None:
                row.append('{:.2f}'.format(val['error']))
            else:
                row.append('')                
        header.append(row)

    return base_report.data_table(header, width, style, repeatRows=6)

def tnpa_2996_2020_clock(data):
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

    return base_report.data_table(header, width, style, repeatRows=5)

def tnpa_2996_2020_extra(data):
    res = extra_block()
    header, style, width = res
    n = 0
    for mac, place, m in data:
        n += 1
        row = [str(n), str(place), str(mac), '']
        header.append(row)
    return base_report.data_table(header, width, style, repeatRows=1)




#--------------

class tnpa_2996_2020(base_report.Report):
    algoritm = tnpa_list.keys()

    def __init__(self, *args, **kwargs):
        res = super().__init__(*args, pageNumbers = True, 
                               footer = '№ {}-СЭТ/{}'.format(kwargs['info']['id'],kwargs['info']['time'].year), 
                               **kwargs)
        return res
    
    def addProtocol(self, number, model, customer, lab_name, lab_descr, place, date, unit, t, f, p):
        self.add_protocol()

        self.tnpa = tnpa_list[model]
        self.elements.extend([
            base_report.page_header1(number, 'счетчиков электрической энергии трехфазных многофункциональных', self.tnpa['model']),
            base_report.org_info(customer, lab_descr, place),
            base_report.report_info(date, self.tnpa['name']),
            base_report.unit_info(unit),
            base_report.measure_info(t, f, p),
            base_report.add_text('Результаты поверки:'),
            ])

    def endProtocol(self, fio):
        if self.tnpa['R']:
            self.elements.append(tnpa_2996_2020_com_ar(self.tnpa['mod'], self.devs))
        else:
            self.elements.append(tnpa_2996_2020_com_a(self.tnpa['mod'], self.devs))

        if self.tnpa['gen']:
            if self.tnpa['R']:
                self.elements.append(tnpa_2996_2020_com_arm(self.tnpa['mod'], self.devs))
            else:
                self.elements.append(tnpa_2996_2020_com_am(self.tnpa['mod'], self.devs))

        self.elements.append(tnpa_2996_2020_a(self.tnpa['mod'], self.devs, '+'))
        if self.tnpa['gen']:
            self.elements.append(tnpa_2996_2020_a(self.tnpa['mod'], self.devs, '-'))
        if self.tnpa['R']:
            self.elements.append(tnpa_2996_2020_r(self.tnpa['mod'], self.devs, '+'))
            if self.tnpa['gen']:
                self.elements.append(tnpa_2996_2020_r(self.tnpa['mod'], self.devs, '-'))

        for phase in ('A','B','C'):
            self.elements.append(tnpa_2996_2020_p_a(self.tnpa['mod'], self.devs, phase, '+'))
            if self.tnpa['gen']:
                self.elements.append(tnpa_2996_2020_p_a(self.tnpa['mod'], self.devs, phase, '-'))
            if self.tnpa['R']:
                self.elements.append(tnpa_2996_2020_p_r(self.tnpa['mod'], self.devs, phase, '+'))
                if self.tnpa['gen']:
                    self.elements.append(tnpa_2996_2020_p_r(self.tnpa['mod'], self.devs, phase, '+'))

        for phase in ('A','B','C'):
            self.elements.append(tnpa_2996_2020_p_ui(self.tnpa['mod'], self.devs, phase))

        self.elements.append(tnpa_2996_2020_clock(self.devs))

        self.elements.append(base_report.add_text('Дополнительные сведения'))
        self.elements.append(tnpa_2996_2020_extra(self.devs))
        
        self.elements.append(base_report.signature(fio))