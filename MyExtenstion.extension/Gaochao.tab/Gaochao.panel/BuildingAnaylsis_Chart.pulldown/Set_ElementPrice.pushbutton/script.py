# -*- coding: utf-8 -*-
__doc__="根据定额设置构件价格"

import rpw
from rpw import revit, DB, UI,db,doc

import json

from Helper import *
import urllib
import urllib2

from Collector.ElementCollector import GetElementsByAssemblyCode
from pyrevit import forms

from ElementPrice import ApiPrice

import csv

#param_id = DB.ElementId(DB.BuiltInParameter.UNIFORMAT_CODE)

#parameter_filter = rpw.db.ParameterFilter(param_id, begins='14')
#allElement = rpw.db.Collector(parameter_filter=parameter_filter, is_type=True).get_elements(wrapped=True)
#Select Assembly Coder
#class MyOption(forms.TemplateListItem):
#	@property
#	def name(self):
#		return "AssemblyName{}AssemblyCode:{}".format(self.get_Parameter(DB.BuiltInParameter.UNIFORMAT_CODE).AsString(),
#													  self.get_Parameter(DB.BuiltInParameter.UNIFORMAT_DESCRIPTION).AsString())


#items = [MyOption(i) for i in allElement]

#AssemblyCoder = forms.SelectFromList.show(items, title="类型选择", button_name='确认')

#AssemblyCoder=AssemblyCoder.get_Parameter(DB.BuiltInParameter.UNIFORMAT_CODE).AsString()


#keynotetable = db.Collector(of_class='KeynoteTable',is_type=False).get_elements(wrapped=False)[0]



#elements=GetElementsByAssemblyCode(AssemblyCoder)
_elements=revit.pick_element()
# Set Prcie to Single Elment
def SetElementTypePrice(element):

	_keynote=element.unwrap().get_Parameter(DB.BuiltInParameter.KEYNOTE_PARAM)
	if _keynote.AsString()!=None and _keynote.AsString()!='' :
		keynote = _keynote.AsString()
		print(keynote)
	else:
		keynote=None
		forms.alert('请为Id:{}添加KeyNote'.format(element.unwrap().Id), exitscript=False)
		return False
	mcoder=keynote
	c=ApiPrice()

	out=c.BPrices(mcoder)
	if len(out)==0:
		forms.alert('该构件无概算价格', exitscript=False)
		return False
	items =out

	class MyOption(forms.TemplateListItem):
		@property
		def name(self):
			return "定额编号:{}项目名称:{}概算基价:{}{}".format(self.get('coder'),self.get('coder_name'),self.get('bprice'),self.get('unit'))

	items=[MyOption(i) for i in items]

	res = forms.SelectFromList.show(items, title=element.name, button_name='选择定额')
	with revit.Transaction('Fake load'):
		cost = element.parameters['Cost'].value=res.get('bprice')
		sub=element.parameters['BudgetCode'].value=res.get('coder')
		print(res.get('coder'))
		forms.alert('{}定额添加完成'.format(items[0].get('coder_name')), exitscript=False)
	return True

# you can also pass a list of objects
# the form will show the str(object) of the objects in the list


for i in [_elements]:
	i=db.Element(i).type

	if i.parameters['BudgetCode'].value==None or i.parameters['BudgetCode'].value=='':

		if SetElementTypePrice(i):
			print("{}Set Price Success".format(i.name))
		else:
			print("break")
			break

	else:
		print('{} 已经都包含了定额价格')