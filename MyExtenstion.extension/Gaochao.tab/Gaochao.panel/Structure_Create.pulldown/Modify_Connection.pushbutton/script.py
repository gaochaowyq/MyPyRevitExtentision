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

Picked2= uidoc.Selection.PickObjects(UI.Selection.ObjectType.Element)
Picked_Selection2=[]
for i in Picked2:
	print(i)
	PickedElementId2=i.ElementId
	Picked=db.Element.from_id(PickedElementId2)
	Picked_Selection2.append(Picked.unwrap())
	

picked=Picked_Selection.unwrap()
picked2=Picked_Selection2


def GetConnectionHandlerTypeGuid(conn,doc):
	if conn ==None or doc ==None:
		return System.Guid.Empty

	typeId = conn.GetTypeId()
	#typeId = conn.Id
	if typeId == DB.ElementId.InvalidElementId:
		return System.Guid.Empty

	connType =doc.GetElement(typeId)
	if connType == None or connType.ConnectionGuid ==None:
		return System.Guid.Empty

	return connType.ConnectionGuid



def GetSchema(doc,connection):    
	schema =None

	guid =GetConnectionHandlerTypeGuid(connection, doc)
	if guid != None and guid !=System.Guid.Empty:
		schema=DB.ExtensibleStorage.Schema.ListSchemas()
		for i in schema:
			if i.GUID==guid:
				return i
#get Schema from Element    
masterSchema = GetSchema(doc,picked)
fields = masterSchema.ListFields()
masterEnt = picked.GetEntity(masterSchema)
for i in fields:
	fieldtype=i.ValueType
	if i.ValueType==System.String:
		parameters=masterEnt.Get[IList[System.String]](i)
		
		#print(parameters)	
	

@rpw.db.Transaction.ensure('ModifyConnection')
def ModifyConnection():
	
	masterSchema = GetSchema(doc,picked)
	fields = masterSchema.ListFields()
	masterEnt = picked.GetEntity(masterSchema)
	for i in picked2:
		i.SetEntity(masterEnt)
	
ModifyConnection()
#print("Done")





	