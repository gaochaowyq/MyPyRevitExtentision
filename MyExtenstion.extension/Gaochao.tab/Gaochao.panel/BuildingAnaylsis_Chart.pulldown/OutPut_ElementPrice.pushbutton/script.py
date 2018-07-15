# -*- encoding: utf-8 -*-
__doc__="设置构件价格"
import os
import traceback
import collections
import sys
import rpw
from rpw import revit, DB, UI,db,doc
from System.Collections.Generic import List
import json
import subprocess as sp
#from Adaptor import BAT_ElementMaterial
#from Viewer.MyChart import MyCharts
import Helper
from Viewer.MyChart import MyCharts
from Adaptor.CovertToChartFormat import CoverToChartFormat as CTC
import pickle
import csv,codecs, cStringIO
import traceback
from BAT_Element_Cover import *
#Get Inside Wall And Outside Wall then show in on the Pin Table
CurrentView=doc.ActiveView


_filename=os.path.basename(doc.PathName)


#所有的价格按照m3计算
###################################################
#10 11
OUTPUT=[
	{"Get_Stu_Base":"14-20.10"},
	{"Get_Stu_CO_Floors":"14-20.20.03"},
	{"Get_Stu_ST_Framings":"14-20.30.06"},
	{"Get_Stu_ST_Columns":"14-20.30.03"},
	{"Get_Stu_CO_Columns":"14-20.20.09"},
	{"Get_Stu_CO_Walls":"14-20.20.15"},
	{"Get_Arc_Element_Walls":"14-10.20.03"},
	{"Get_Arc_Element_Columns":"14-10.20.06"},
	{"Get_Arc_Element_Door":"14-10.20.09"},
	{"Get_Arc_Element_Window":"14-10.20.12"},
	{"Get_Arc_Element_Roofs":"14-10.20.15"},
	{"Get_Arc_Element_Floors":"14-10.20.18"},
	{"Get_Arc_Element_Ceiling":"14-10.20.24"},
	{"Get_Arc_Element_Planting_Place":"14-10.10.18.12"},
	{"Get_Arc_Element_CurtainWall_Element":"14-10.20.21.03"},
	{"Get_Arc_Element_Canopy":"14-10.20.48.12"},
	{"Get_MEP_Ducts":"14-30.40.03"},
	{"Get_MEP_Pipe":"14-30.20.03"},
	{"Get_MEP_SupplyPipe":"14-40.10.03"},
	{"Get_MEP_DrainPipe":"14-40.20.03"},
	{"Get_MEP_FirePipe":["14-40.30.09","14-40.30.12","14-40.30.15"]},
	{"Get_MEP_Conduit":"14-50.40"}
		]
CutomOutPut={
"Get_Custom_HAVC_Place":"14-60.10"
}
#14 40 10 03
#14 40 20 03
#14 40 30

# 获取所有表14的Element
#OUTPUT.update(CutomOutPut)
o=[]
for i in OUTPUT:

	c=eval(i.keys()[0])().OutPut_Total()
	try:
		output=CTC(c)
		output=output.OutPut()
		c=MyCharts(output)
		c.test1_chart()
		JsonFile=c.ToJson()
		o.append(JsonFile)
	except:
		pass
FilePath=r'c:/BAT_OUT'
if os.path.exists(FilePath):
	pass
else:
	os.makedirs(FilePath)

Path="{rootpath}//{filename}.svf.lln".format(rootpath=FilePath,filename=_filename)

with open(Path,'wb') as f:
	pickle.dump(o,f)
	print("{filename}.svf.lln is Writed in {Path}".format(filename=_filename,Path=Path))

	






