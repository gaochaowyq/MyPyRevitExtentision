# -*- coding: utf-8 -*-
__doc__="返回选择物体的类型"
import pyrevit
import clr
import rpw
from rpw import db,doc
from pyrevit import DB,UI,_HostApplication
from  Helper import *

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
			{"Guid":"",
			 "UserData":
				[
					{"Category":"","Name":"","Value":""},
					{"Category":"","Name":"","Value":""},
					{"Category":"","Name":"","Value":""}
				]
			}
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

def LocationToValue(ElementLocation):
	if isinstance(ElementLocation,DB.LocationCurve):
		s=ElementLocation.Curve.GetEndPoint(0)
		e = ElementLocation.Curve.GetEndPoint(1)

		return [[int(s.X),int(s.Y),int(s.Z)],[int(e.X),int(e.Y),int(e.Z)]]
	else:
		print("bad")


def AddGISLocation_Wall(WallElement):
	WrapedWall=db.Element(WallElement)



	LocationCurve=WallElement.Location



	StartPoint=LocationToValue(LocationCurve)[0]
	EndPoint=LocationToValue(LocationCurve)[1]



	Location={"SP":StartPoint,"EP":EndPoint,"BL":"","BO":"","TL":"","TO":""}


	Location["BL"]=WrapedParameterValue(WrapedWall.parameters[ParameterName.WALL_BASE_CONSTRAINT])
	Location["BO"] =WrapedParameterValue(WrapedWall.parameters[ParameterName.WALL_BASE_OFFSET])
	Location["TL"] =WrapedParameterValue(WrapedWall.parameters[ParameterName.WALL_HEIGHT_TYPE])
	Location["TO"] =WrapedParameterValue(WrapedWall.parameters[ParameterName.WALL_TOP_OFFSET])
	with db.Transaction('add Gis Location'):
		WrapedWall.parameters["GISLocation"]=Location

for i in Walls:

	AddGISLocation_Wall(i)











