# -*- coding: utf-8 -*-
__doc__="返回选择物体的类型"
import rpw
from rpw import revit, DB, UI,db,doc
import Helper


import json
#Selection Element
selection = rpw.ui.Selection()

Elements=[]
for i in selection:
	Elements.append(db.Element(i))
#Make mark
@rpw.db.Transaction.ensure('MakeMark')
def MakeMark(Elements):
	for i in range(0,len(Elements)):		
		Elements[i].parameters['Mark']=i
		print("{}is done".format(i))
#Read Heigth
with open(r'E:\0_2018项目\20180102 海新广场项目\Tem\MulionHight','r') as f:
	Height=json.loads(f.read())



#Change Height
@rpw.db.Transaction.ensure('Change Heigth')
def Change_Heigth(Elements):
	for i in range(0,len(Elements)):
		for c in Elements:
			if c.parameters['Mark']==str(i+1):
				c.parameters['Top Offset']=Helper.CovertToMM(Height[i])
				print("{}is done".format(i))


Change_Heigth(Elements)