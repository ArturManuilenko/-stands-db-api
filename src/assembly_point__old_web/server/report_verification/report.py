import report_verification.base_report as base_report
from report_verification.tnpa_2948_2020 import tnpa_2948_2020_com, tnpa_2948_2020_A, tnpa_2948_2020_R, tnpa_2948_2020_extra

from report_verification.tnpa_2948_2020 import tnpa_2948_2020
from report_verification.tnpa_2996_2020 import tnpa_2996_2020
from report_verification.stb_8046_2015 import stb_8046_2015
from report_verification.tnpa_xxxxx_2021 import tnpa_xxxxx_2021

tnpa_list = {
    'SM204 5-60 L AR':{'model':'SM', 'name':'МРБ МП.2948-2020', 'R':True, 'N':False, 'gen':True},
    'SM204 5-100 L AR':{'model':'SM', 'name':'МРБ МП.2948-2020', 'R':True, 'N':False, 'gen':True},
    'SM204 5-60 L A':{'model':'SM', 'name':'МРБ МП.2948-2020', 'R':False, 'N':False, 'gen':True},
    'SM204 5-100 L A':{'model':'SM', 'name':'МРБ МП.2948-2020', 'R':False, 'N':False, 'gen':True},
    'SM204 5-60 LN AR':{'model':'SM204 5(60) 1/1 D.R.O.RF.L', 'name':'МРБ МП.2948-2020', 'R':True, 'N':True, 'gen':True},
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


class Document:
    def __init__(self, file):
        self.file = file
        self.reports={}
        self.reports.update({key:tnpa_2948_2020 for key in tnpa_2948_2020.algoritm})
        self.reports.update({key:tnpa_2996_2020 for key in tnpa_2996_2020.algoritm})   
        self.reports.update({key:stb_8046_2015 for key in stb_8046_2015.algoritm})
        self.reports.update({key:tnpa_xxxxx_2021 for key in tnpa_xxxxx_2021.algoritm})

    def add_report(self, type, id, time):
        r = self.reports.get(type)
        return r(self.file, info = {'id':id, 'time':time})


class Report:
    def __init__(self, file):
        self.file = file
        self.elements=[]

    def addProtocol(self, number, model, customer, lab, place, date, unit, t, f, p):
        self.tnpa = tnpa_list[model]
        self.devs = []

        if len(self.elements) > 0:
           self.elements.append(base_report.page_break())
        self.elements.extend([
            base_report.page_header(number, self.tnpa['model']),
            base_report.org_info(customer, lab, place),
            base_report.report_info(date, self.tnpa['name']),
            base_report.unit_info(unit),
            base_report.measure_info(t, f, p),
            base_report.add_text('Результаты поверки:'),
            ])

    def addDevice(self, mac, place, measures):
        self.devs.append((mac, place + 1, measures))

    def endProtocol(self, fio):
        self.elements.append(tnpa_2948_2020_com(self.devs))
        self.elements.append(base_report.add_text(''))
        
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

        self.elements.append(base_report.add_text(''))
        self.elements.append(tnpa_2948_2020_extra(self.devs))

        self.elements.append(base_report.signature(fio))

    def save(self):
        base_report.save(self.file, self.elements)