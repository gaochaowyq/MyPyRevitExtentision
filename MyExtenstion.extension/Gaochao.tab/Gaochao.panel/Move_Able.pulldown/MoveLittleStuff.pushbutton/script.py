# -*- coding: utf-8 -*-
__doc__="返回选择物体的类型"
import time
from threading import Timer  
import time  
import rpw
from rpw import revit, db, ui,DB,UI
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button
import json

from MyLib import Helper
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
#doc = __revit__.ActiveUIDocument.Document
doc =revit.doc

Picked= uidoc.Selection.PickObject(UI.Selection.ObjectType.Element)
PickedElementId=Picked.ElementId
Picked_Selection=db.Element.from_id(PickedElementId)

MoveElement=Picked_Selection
c=1
timer_interval=1  
def delayrun():
	c=c+1
	print(running)
	print(c)
  
t=Timer(timer_interval,delayrun)  
t.start()
if c==5:
	t.cancel()



@rpw.db.Transaction.ensure('CreateBeam')
def CreateBeam(Curves,FamilySymbol,Level,StructureType):
	for i in Curves:
		doc.Create.NewFamilyInstance(i,FamilySymbol,Level,StructureType)

print(MoveElement)

	


		
		






	