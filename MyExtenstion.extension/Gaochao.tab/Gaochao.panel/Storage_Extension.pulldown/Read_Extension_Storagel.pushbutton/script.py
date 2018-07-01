# -*- coding: utf-8 -*-
__doc__="返回选择物体的类型"
import System
import rpw
from rpw import revit, db, ui,DB,UI
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button
import json

from MyLib import Helper
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument


Picked= uidoc.Selection.PickObject(UI.Selection.ObjectType.Element)
PickedElementId=Picked.ElementId
Picked_Selection=db.Element.from_id(PickedElementId).unwrap()
#信息输入部分




schema=DB.ExtensibleStorage.Schema.Lookup(System.Guid("720080CB-DA99-40DC-9415-E53F280AA1FD"))
retrievedEntity = Picked_Selection.GetEntity(schema)
cc=schema.GetField("New_WireSpliceLocation")


retrievedData =retrievedEntity.Get[type(DB.XYZ())](cc,DB.DisplayUnitType.DUT_METERS)

print(retrievedData)

		
		






	