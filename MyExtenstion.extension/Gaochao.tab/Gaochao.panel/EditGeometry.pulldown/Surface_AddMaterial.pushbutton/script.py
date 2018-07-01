# -*- coding: utf-8 -*-
__doc__="返回选择物体的类型"
import rpw
from rpw import revit, db, ui,DB,UI
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button
import json
import sys

from MyLib import Helper
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

print(sys.path)
Picked= uidoc.Selection.PickObject(UI.Selection.ObjectType.Face)
PickedElementId=Picked.ElementId
print(PickedElementId)

Picked_Selection=db.Element.from_id(PickedElementId)
#信息输入部分

Picked_Geometry=Picked_Selection.unwrap().get_Geometry(DB.Options())

enum1=Picked_Geometry.GetEnumerator()
print(enum1)

for i in enum1:
	newenum1=i.GetInstanceGeometry()
	for c in newenum1:
		print(c.Faces.Size)
		for m in c.Faces:
			try:
				print(m.Points)
			except:
				pass
	

		
		






	