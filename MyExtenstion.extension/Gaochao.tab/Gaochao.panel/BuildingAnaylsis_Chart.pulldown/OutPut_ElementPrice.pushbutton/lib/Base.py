# -*- encoding: utf-8 -*-
import rpw
import traceback
from rpw import db,doc
from pyrevit import DB
def CovertToM3(input):
    return input/35.3147248
def CovertToM2(input):
    return input/10.7639104
def CovertToM(input):
    return input/3.2808399
def CovertToMM(input):
    return round(float(input/0.0032808),0)

class GetAllBase(object):
    def __init__(self):
        self.param_id = DB.ElementId(DB.BuiltInParameter.UNIFORMAT_CODE)
        #KEYNOTE_PARAM
        self.param_id_Keynote = DB.ElementId(DB.BuiltInParameter.KEYNOTE_PARAM)

    def Elements(self):
        if hasattr(self, 'NotContainAssembleCode'):
            parameter_filter = rpw.db.ParameterFilter(self.param_id, begins=self.AssembleCode,
                                                      not_contains=self.NotContainAssembleCode)
            collector = rpw.db.Collector(parameter_filter=parameter_filter, is_type=False).get_elements(wrapped=True)
        else:
            if isinstance(self.AssembleCode,str):
                parameter_filter = rpw.db.ParameterFilter(self.param_id, begins=self.AssembleCode)
                collector = rpw.db.Collector(parameter_filter=parameter_filter, is_type=False).get_elements(wrapped=True)
            else:
                collector=[]
                for i in self.AssembleCode:
                    parameter_filter = rpw.db.ParameterFilter(self.param_id, begins=i)
                    _collector = rpw.db.Collector(parameter_filter=parameter_filter, is_type=False).get_elements(wrapped=True)
                    for i in _collector:
                        collector.append(i)
        return collector

    # GetAllElementsCosts As Lit
    def GetCosts(self):
        try:
            return [i.type.parameters['Cost'].value for i in self.Elements()]
        except:
            return [i.type.parameters['成本'].value for i in self.Elements()]


    def GetAC(self):
        try:
            return [i.type.parameters['Assembly Code'].value for i in self.Elements()]
        except:
            return [i.type.parameters['部件代码'].value for i in self.Elements()]


    def GetACName(self):
        return [i.type.parameters['Assembly Description'].value.encode('GB2312') for i in self.Elements()]

    def GetClassName(self):
        return [self.ClassName.encode('GB2312') for i in self.Elements()]

    def Name(self):
        UnwrapedElement = [i.unwrap() for i in self.Elements()]
        return [i.Name.encode('GB2312') for i in UnwrapedElement]

    def GetQutity(self):
        if self.unit == 'm2':
            try:
                return [CovertToM2(i.parameters['Area'].value) for i in self.Elements()]
            except:
                return [CovertToM2(i.parameters['面积'].value) for i in self.Elements()]


        elif self.unit == 'm3':
            try:
                return [CovertToM3(i.parameters['Volume'].value) for i in self.Elements()]
            except:
                return [CovertToM3(i.parameters['体积'].value) for i in self.Elements()]
        elif self.unit == 't':
            try:
                return [CovertToM3(i.parameters['Volume'].value)*7.85 for i in self.Elements()]
            except:
                return [CovertToM3(i.parameters['体积'].value)*7.85 for i in self.Elements()]


        elif self.unit == 'm':
            value=[]
            for i in self.Elements():
                try :
                    try:
                        c=CovertToM(i.parameters['Length'].value)
                    except:
                        c = CovertToM(i.parameters['长度'].value)

                    value.append(c)
                except:
                    value.append(0)
            return value
        elif self.unit == 'Count':
            c = []
            for i in self.Elements():
                c.append(1)
            return c

    def OutPut(self):
        output = []

        for i, c, b, d, f in zip(self.GetAC(), self.GetClassName(), self.GetCosts(), self.Name(), self.GetQutity()):
            _dict = {}
            _dict['Assembly Code'] = i
            _dict['Assembly Description'] = c
            _dict['Cost'] = b
            _dict['Unit'] = self.unit
            _dict['ElementName'] = d
            _dict['Qutity'] = f
            output.append(_dict)
        return output

    def OutPut_Total(self):
        all = self.OutPut()
        tem = []
        try:
            for i in all:
                if i['ElementName'] in tem:
                    pass
                else:
                    tem.append(i['ElementName'])
            newout = []
            for i in tem:
                new = {'Cost': 0, 'Count': 0, 'Qutity': 0}
                for c in all:
                    if c['ElementName'] == i:
                        new['ElementName'] = c['ElementName']
                        new['Assembly Code'] = c['Assembly Code']
                        new['Assembly Description'] = c['Assembly Description']
                        new['Unit'] = c['Unit']
                        new['Qutity'] = new['Qutity'] + c['Qutity']
                        new['Cost'] = new['Cost'] + c['Cost']
                        new['Count'] = new['Count'] + 1
                newout.append(new)
            return newout
        except:
            traceback.print_exc()
            #############################################################