# -*- encoding: utf-8 -*-
__doc__ = "设置构件价格"
import os
import traceback
import sys
import rpw
from rpw import revit, DB, UI, db, doc
from System.Collections.Generic import List
import json
import subprocess as sp
# from Adaptor import BAT_ElementMaterial
# from Viewer.MyChart import MyCharts
import Helper
from Viewer.MyChart import MyCharts, LineChart
from Adaptor.CovertToChartFormat import CoverToChartFormat as CTC
import pickle
import csv, codecs, cStringIO
import traceback

# Get Inside Wall And Outside Wall then show in on the Pin Table
CurrentView = doc.ActiveView
_filename = os.path.basename(doc.PathName)
c=db.Collector(of_category='OST_Rooms').get_elements()



# 所有的价格按照m3计算
###################################################
# 10 11
OUTPUT = {
	"Get_Stu_Base": "14-20.10",
	"Get_Stu_CO_Floors": "14-20.20.03",
	"Get_Stu_ST_Framings": "14-20.30.06",
	"Get_Stu_ST_Columns": "14-20.30.03",
	"Get_Stu_CO_Columns": "14-20.20.09",
	"Get_Stu_CO_Walls": "14-20.20.15",
	"Get_Arc_Element_Walls": "14-10.20.03",
	"Get_Arc_Element_Columns": "14-10.20.06",
	"Get_Arc_Element_Door": "14-10.20.09",
	"Get_Arc_Element_Window": "14-10.20.12",
	"Get_Arc_Element_Roofs": "14-10.20.15",
	"Get_Arc_Element_Floors": "14-10.20.18",
	"Get_Arc_Element_Ceiling": "14-10.20.24",
	"Get_MEP_Ducts": "14-30.40.03",
	"Get_MEP_Pipe": "14-30.20.03",
	"Get_MEP_SupplyPipe": "14-40.10.03",
	"Get_MEP_DrainPipe": "14-40.20.03",
	"Get_MEP_FirePipe": ["14-40.30.09", "14-40.30.12", "14-40.30.15"],
	"Get_MEP_Conduit": "14-50.40"
}


# 14 40 10 03
# 14 40 20 03
# 14 40 30

# 获取所有表14的Element

class Element:
	def __init__(self):
		self.title = 'Whatever'

	def setTitle(self, Title):
		self.title = Title

	def setLabale(self, Labale):
		self.labels = Labale

	def setData(self, Data):
		self.data = Data

	def setDataname(self, Dataname):
		self.DataName = Dataname
#labale = ["first", "second", "third", "forth"]
#data = {"one": [1, 2, 3, 4], "two": [5, 3, 3, 4], "three": [20, 3, 3, 4]}
labale = []
data = {}
for i in c:
	print(CovertToMM(i.parameters['Unbounded Height'].value))



b = []
for i, j in data.items():
	cc = Element()
	cc.setLabale(labale)
	cc.setData(j)
	cc.setDataname(i)
	b.append(cc)

c = LineChart(b)
c.test1_chart()
