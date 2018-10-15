# -*- coding: utf-8 -*-
__doc__="返回选择物体的类型"
import  sys
import rpw
import pyrevit
from rpw import db,doc
from pyrevit import revit,DB,UI,forms,HOST_APP
import System
from System.Collections.Generic import List



picked = revit.pick_element()

for i in picked.get_Geometry(DB.Options ()):
	for c in i.GetInstanceGeometry():
		print(c)


new=List[DB.GeometryObject]()
new.Add(c)
categoryId =DB.ElementId(DB.BuiltInCategory.OST_Floors)
with revit.Transaction("Convert ACIS to FreeFrom"):
	ds = DB.DirectShape.CreateElement(doc, categoryId)
	ds.SetShape(new)
	ds.Name = "MyShape"
	

		
		






	