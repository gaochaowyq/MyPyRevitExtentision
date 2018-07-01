# -*- coding: utf-8 -*-
__doc__="返回选择物体的类型"
from pyrevit import revit, DB
from pyrevit import forms
import rpw

curdoc=revit.doc

piped=revit.pick_element()


wraped=rpw.db.Element(piped)

c=wraped.unwrap()

l=c.get_Parameter(DB.BuiltInParameter.RBS_CALCULATED_SIZE).AsString()

print(l)

#def select_clouds():
#	cl = DB.FilteredElementCollector(revit.doc)
#	Dimesion = cl.OfCategory(DB.BuiltInCategory.OST_Dimensions).WhereElementIsNotElementType()
#	return Dimesion
#c=select_clouds()
#for i in c:
#	print(i.Id)
	
#b=[i for i in c]

	
	
#@rpw.db.Transaction.ensure('Delete')
#def DeleteElement(Element):

#	curdoc.Delete(Element.Id)
#	print("well")

#for i in b:
#	DeleteElement(i)
