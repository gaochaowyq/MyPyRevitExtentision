# -*- coding: utf-8 -*-
__doc__="更具曲面与垂直线创建结构"
import System

from System.Collections.Generic import List, Dictionary,IList
import sys
import clr
import os
import rpw
from rpw import revit, db, ui,DB,UI
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button, Alert
import json

from MyLib import Helper
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

#pick Surface
Picked= uidoc.Selection.PickObject(UI.Selection.ObjectType.Element)
PickedElementId=Picked.ElementId
Picked_Selection=db.Element.from_id(PickedElementId)

parameter=Picked_Selection.parameters.all

Unwrap_Element=Picked_Selection.unwrap()

Picked_Geometry=Unwrap_Element.get_Geometry(DB.Options())

for i in Picked_Geometry:
	try:
		print(Helper.CovertToM2(i.SurfaceArea))
	except:
		print("bad")

#print(Picked_Geometry)





	