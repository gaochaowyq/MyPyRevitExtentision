# -*- coding: utf-8 -*-
__doc__="返回选择物体的类型"
import pyrevit
import clr
import rpw
from rpw import db,doc
from pyrevit import DB,UI,_HostApplication
from  Helper import *
import json as _J
import System
from System.Collections.Generic import List
from pyrevit.framework import Stopwatch
hostapp = _HostApplication(__revit__)
if hostapp.app.Language.ToString()=="English_USA":
	ParameterName=LG_EUN()
elif hostapp.app.Language.ToString()=="Chinese_Simplified":
	ParameterName = LG_CHS()

##############################################################################
OST_WALL=DB.Category.GetCategory(doc,DB.BuiltInCategory.OST_Walls)
OST_StructuralColumns=DB.Category.GetCategory(doc,DB.BuiltInCategory.OST_StructuralColumns)
##############################################################################
#title="根据Accessmbly筛选构件价格"
#description="根据Accessmbly筛选构件价格"
#value=rpw.ui.forms.TextInput(title, default=None, description=description, sort=True, exit_on_close=True)
#Accessmbly_Code=value

Walls  = db.Collector(of_class='Wall',is_type=False).get_elements(wrapped=False)


json={"data":[
		]

}

def WrapedParameterValue(Parameter):
	_type=Parameter.type

	if _type is DB.ElementId:
		value = Parameter.value
		if value.IntegerValue ==-1:
			return None
		else:
			element=db.Element.from_id(value)
			name=element.parameters["Name"].value
			return name
	else:
		value = Parameter.value
		return value


def GetWallData(WallElement):
	Guid=WallElement.UniqueId
	ExportJson={"Guid": Guid,
	 "UserData":
		 [
		 ]
	 }

	_ParameterName_Constrain=[ParameterName.WALL_BASE_CONSTRAINT,ParameterName.WALL_BASE_OFFSET,ParameterName.WALL_HEIGHT_TYPE,ParameterName.WALL_TOP_OFFSET]
	_ParameterName_Quality=[ParameterName.WALL_Length,ParameterName.WALL_Area,ParameterName.WALL_Volume]
	WrapedWall=db.Element(WallElement)

	for i in _ParameterName_Constrain:

		parametername=WrapedWall.parameters[i].name


		parametervalue = WrapedParameterValue(WrapedWall.parameters[i])

		_Constraints = {"Category": "Constrain", "Name": parametername.encode('GB2312'), "Value": parametervalue}
		ExportJson["UserData"].append(_Constraints)
	for i in _ParameterName_Quality:


		try:
			parametername = WrapedWall.parameters[i].name
			parametervalue = WrapedParameterValue(WrapedWall.parameters[i])
		except:
			parametername = i
			parametervalue=None

		_Constraints = {"Category": "Quantity", "Name": parametername, "Value": parametervalue}
		ExportJson["UserData"].append(_Constraints)

	_GIS = {"Category": "GISLocation", "Name": "GISLocation", "Value": WrapedWall.parameters["GISLocation"].value}
	ExportJson["UserData"].append(_GIS)

	return ExportJson




for i in Walls:
	data=GetWallData(i)


	json["data"].append(data)

print(json)
with open('c:\\BAT_ZhaoShangYinhang.json','w') as json_file:

	_J.dump(json,json_file,ensure_ascii=True, encoding='utf-8')












