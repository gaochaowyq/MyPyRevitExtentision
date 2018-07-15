# -*- coding: utf-8 -*-
class Element:
    def __init__(self):
        self.title='钢精混凝土梁(单位 M3)'
    def setTitle(self,Title):
        self.title=Title
    def setLabale(self,Labale):
        self.labels=Labale
    def setData(self,Data):
        self.data=Data


class CoverToChartFormat:
    def __init__(self,data):
        self.data=data

    def OutPut(self):
        Labale=[]
        Data=[]
        for i in self.data:
            Labale.append("{}".format(i['ElementName'].decode('GB2312','strict')))
            Data.append(round(i['Qutity'],1))
        out=Element()
        out.setData(Data)
        out.setLabale(Labale)
        out.setTitle("{} 单位 {}".format(self.data[0]['Assembly Description'].decode('GB2312','strict'),self.data[0]['Unit'].decode('GB2312','strict')))
        return out

