# -*- coding: utf-8 -*-
__doc__="返回选择物体的类型"
import rpw
from rpw import revit, DB, UI,db,doc
from System.Collections.Generic import List
import json

import subprocess as sp
#from MyLib.Adaptor import BAT_Wall
from Adaptor import BAT_ElementMaterial
from Helper import *

#根据Accessmbly Code 筛选构件
title="根据Accessmbly筛选构件价格"
description="根据Accessmbly筛选构件价格"
value=rpw.ui.forms.TextInput(title, default=None, description=description, sort=True, exit_on_close=True)
Accessmbly_Code=value


class GetElementByAccessmblyCode():
	def __init__(self,Accessmbly_Code):
		self.Accessmbly_Code=Accessmbly_Code
	
	def GetAllElement(self):

		param_id = DB.ElementId(DB.BuiltInParameter.UNIFORMAT_CODE )
		param_id2 = DB.ElementId(DB.BuiltInParameter.ALL_MODEL_TYPE_MARK )
		parameter_filter = rpw.db.ParameterFilter(param_id, begins=self.Accessmbly_Code)
		parameter_filter2=rpw.db.ParameterFilter(param_id2,equals='外墙1')
		collector2 =rpw.db.Collector(parameter_filter=parameter_filter2,is_type=False)

		collector =rpw.db.Collector(parameter_filter=parameter_filter,is_type=False).wrapped_elements

		return collector
	
	def GetAllElementCost(self):
		cost=[]

		for i in self.GetAllElement():
			symbol=i.type
			cost.append(symbol.parameters['Cost'].value)
		return cost
	def GetAllElementquantity(self):
		quantity=[]

		for i in self.GetAllElement():
			try:
				
				quantity.append(CovertToM3(i.parameters['Volume'].value))
			except:
				quantity.append(CovertToM2(i.parameters['Area'].value))
				
		return quantity
	def GetTotalCost(self):
		singlecost=self.GetAllElementCost()

		singleQuantity=self.GetAllElementquantity()
		def add(a,b):
			return a*b
		_result=map(add,singlecost,singleQuantity)
		print(sum(_result))
		result=round((sum(_result)/10000),2)
		
		return result*1.07
		

Element=GetElementByAccessmblyCode(Accessmbly_Code)
print(Element.GetAllElement())

OneWall=Element.GetAllElement()[0].unwrap()

MyWall=BAT_ElementMaterial.BAT_ElementMaterial(OneWall)

name=MyWall.GetMaterialAreaWithName()
print(name)


#for i in name:
#	print(i['name'])
print("万元")


		