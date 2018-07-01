# -*- coding: utf-8 -*-
__doc__="根据AssemblyCode返回构件"
import rpw
from rpw import revit, DB, UI,db,doc
from System.Collections.Generic import List
import json

from pyrevit.forms import CommandSwitchWindow
import subprocess as sp

#根据Accessmbly Code 筛选构件
title="根据Accessmbly筛选构件价格"
description="根据Accessmbly筛选构件价格"
value=rpw.ui.forms.TextInput(title, default=None, description=description, sort=True, exit_on_close=True)
Accessmbly_Code=value

#Separat Accessmbly_Code

class GetElementByAccessmblyCode():
	def __init__(self,Accessmbly_Code):
		self.Accessmbly_Code=Accessmbly_Code
	
	def GetAllElement(self):

		param_id = DB.ElementId(DB.BuiltInParameter.UNIFORMAT_CODE )
		parameter_filter = rpw.db.ParameterFilter(param_id, begins=self.Accessmbly_Code)
		collector =rpw.db.Collector(parameter_filter=parameter_filter,is_type=False).get_elements(wrapped=True)
		element_set = rpw.db.ElementSet(collector)
		element_set.select()
		return True
	
		

Element=GetElementByAccessmblyCode(Accessmbly_Code)
Element.GetAllElement()

		