# -*- coding: utf-8 -*-
__doc__="分析设计中内墙与外墙的量"
import os
import sys
import rpw
from rpw import revit, DB, UI,db,doc
from System.Collections.Generic import List
import json
import subprocess as sp
from Adaptor import BAT_ElementMaterial
from Viewer.MyChart import MyCharts
import Helper
import csv
#reload(sys)
#sys.setdefaultencoding('utf-8')
#Get Inside Wall And Outside Wall then show in on the Pin Table
CurrentView=doc.ActiveView

def CovertToM3(input):
	return input/35.3147248
def CovertToM2(input):
	return input/10.7639104
def CovertToM(input):
	return input/3.2808399
#所有的价格按照m3计算	
_filename=rpw.ui.forms.select_file('csv(*.csv)|*.csv')
filename=_filename
with open(filename,'rb') as csvfile:
	reader=csv.reader(csvfile)
	_rows= [row for row in reader]
Price=_rows


# read cal from csv file
class Element:	
	def __init__(self,Input):
		self.input=Input
	def Get_Accessmbly_Code(self):
		return self.input[0]
	def Get_Price(self):
		return self.input[1]
	def Get_Unit(self):
		return self.input[2]
	def Get_Name(self):
		return self.input[3]
	def Get_Tax(self):
		return self.input[5]
	def Get_Laber(self):
		return self.input[4]

class Element_Material(object):
	def __init__(self):
		self.matid=''
		self.matname=''
		self.matarea=''
	def __str__(self):
		return '{}'.format(self.matname)
# 根据AccseemblyCode 获取全部构件及相关属性
class GetElementByAccessmblyCode():
	def __init__(self,Element):
		self.Accessmbly_Code=Element.Get_Accessmbly_Code()
		self.Element_Price=Element.Get_Price()
		self.Element_Unit=Element.Get_Unit()
		self.Element_Tax=Element.Get_Tax()
		self.Element_Laber=Element.Get_Laber()
	#获取Element
	def GetAllElement(self):
		
		param_id = DB.ElementId(DB.BuiltInParameter.UNIFORMAT_CODE )
		parameter_filter = rpw.db.ParameterFilter(param_id, begins=self.Accessmbly_Code)
		collector =rpw.db.Collector(parameter_filter=parameter_filter,is_type=False).wrapped_elements
		
		return collector
	#从模型获取Element价格
	def GetAllElementCost(self):
		cost=[]

		for i in self.GetAllElement():
			symbol=i.type
			cost.append(symbol.parameters['Cost'].value)
		return cost
	#从Input获取Element价格（综合价格）
	def GetAllElementCost_FromInput(self):
		cost=[]

		for i in self.GetAllElement():
			cost.append(self.Element_Price+self.Element_Laber)
		return cost
	#获取Element量 体积
	def GetAllElementquantity_M3(self):
		quantity=[]
		for i in self.GetAllElement():
			try:
				quantity.append(CovertToM3(i.parameters['Volume'].value))				
			except:
				break
		return quantity

	# 获取Element量 面积
	def GetAllElementquantity_M2(self):
		quantity=[]

		for i in self.GetAllElement():
			try:
			
				quantity.append(CovertToM2(i.parameters['Area'].value))
			except:
				break
		return quantity

	# 获取Element量 长度
	def GetAllElementquantity_length(self):
		quantity=[]

		for i in self.GetAllElement():
			try:
				quantity.append(CovertToM(i.parameters['Length'].value))
			except:
				break
		return quantity
	#TODO 获取Element量 公斤
	def GetAllElementquantity_Kg(self):
		pass	

	# TODO 获取Element量 个数
	def GetAllElementquantity_Num(self):
		quantity=[]
		for i in self.GetAllElement():
			try:				
				quantity.append(1)
			except:
				print(i)
		return quantity		
	#计算总价
	def GetTotalCost(self):
		singlecost=self.GetAllElementCost()
		if self.Element_Unit=='yuan/m3':
			singleQuantity=self.GetAllElementquantity_M3()
		elif self.Element_Unit=='yuan/m2':
			singleQuantity=self.GetAllElementquantity_M2()
		elif self.Element_Unit=='yuan/kg':
			singleQuantity=self.GetAllElementquantity_Kg()
		elif self.Element_Unit=='yuan/length':
			singleQuantity=self.GetAllElementquantity_length()
		elif self.Element_Unit=='yuan/number':
			singleQuantity=self.GetAllElementquantity_Num()
		
		def add(a,b):
			return a*b
		_result=map(add,singlecost,singleQuantity)
		result=round((sum(_result)/10000),2)
		
		return result*(1+float(self.Element_Tax))
	#获取量
	def Quantity_With_Unit(self):
		c=self.Element_Unit[5:]
		if self.Element_Unit=='yuan/m3':
			singleQuantity=self.GetAllElementquantity_M3()
		elif self.Element_Unit=='yuan/m2':
			singleQuantity=self.GetAllElementquantity_M2()
		elif self.Element_Unit=='yuan/kg':
			singleQuantity=self.GetAllElementquantity_Kg()
		elif self.Element_Unit=='yuan/length':
			singleQuantity=self.GetAllElementquantity_length()
		elif self.Element_Unit=='yuan/number':
			singleQuantity=self.GetAllElementquantity_Num()
		_result="{}{}".format(sum(singleQuantity),c)
		
		return _result
	def GetAllMaterial(self):
		c=[]
		for i in self.GetAllElement():
			NewElement=BAT_ElementMaterial.BAT_ElementMaterial(i)
			c.append(NewElement.GetMaterialAreaWithName())
		return c
	
# Get Result For Chart and run allcode
class OutPut:
	def __init__(self,Input):
		self.Input=Input
		self.title='WhatEverMyLinke'
		self.labels = self.Get_All_Name()
		self.data = self.Get_All_Price()
	
	def Get_All_AccessmblyCode(self):
		c=[]
		for i in self.Input:
			c.append(i[0])
		return c
	def Get_All_Name(self):
		c=[]
		for i in self.Input:
			c.append(i[3])
		return c
	def Get_All_Price(self):
		c=[]
		for i in self.Input:
			_Price=GetElementByAccessmblyCode(Element(i))
			Price=_Price.GetTotalCost()
			c.append(Price)
		return c
	def Get_All_Quatity(self):
		c = []
		for i in self.Input:
			_Quatity = GetElementByAccessmblyCode(Element(i))
			Price = _Quatity.Quantity_With_Unit()
			c.append(Price)
		return c
	#save all data as dictory
	def SaveAsDic(self):
		cc=[]
		for a,b,c in zip(self.Get_All_Name(),self.Get_All_Quatity(),self.Get_All_Price()):

			dic={'name':a.decode('unicode_escape'),'quantity':b,'price':c}
			cc.append(dic)
		return cc
	def GetMaterial(self):
		c=[]
		for i in self.Input:
			Elements=GetElementByAccessmblyCode(Element(i))
			Material=Elements.GetAllMaterial()
			c.append(Material)
		return c

allelement=[]
Element1=OutPut(Price)




#ditc=NewTest.SaveAsDic()
#Write=WriteToCSV.WriteToCSV("c:/2.csv",ditc)
#Write.Write()


#输入的元素


c=MyCharts(Element1)
c.test1_chart()
#Draw Result
