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



@rpw.db.Transaction.ensure('CreatExtensionStorage')
def CreatExtensionStorage(wall,dataToStore):
	schemaBuilder=DB.ExtensibleStorage.SchemaBuilder(System.Guid("d64e3bab-7b93-415a-a20a-4d09ec106aaa"))
	schemaBuilder.SetReadAccessLevel(DB.ExtensibleStorage.AccessLevel.Public)
	schemaBuilder.SetWriteAccessLevel(DB.ExtensibleStorage.AccessLevel.Public)
	#schemaBuilder.SetVendorId("ADSK")
	schemaBuilder.SetSchemaName("LastTrySchema")
	fieldBuilder = schemaBuilder.AddSimpleField("LastTrySchema", DB.XYZ().GetType())
	fieldBuilder.SetUnitType(DB.UnitType.UT_Length)
	fieldBuilder.SetDocumentation("a wall.")
	schema = schemaBuilder.Finish()

	entity =DB.ExtensibleStorage.Entity(schema)
	fieldSpliceLocation = schema.GetField("LastTrySchema")
	entity.Set[DB.XYZ](fieldSpliceLocation, dataToStore, DB.DisplayUnitType.DUT_METERS)
	wall.SetEntity(entity)
	#gedatabace
	retrievedEntity = wall.GetEntity( schema )
	retrievedData = retrievedEntity.Get[DB.XYZ](schema.GetField( "LastTrySchema"), DB.DisplayUnitType.DUT_METERS)
	print(retrievedData)
	
def ReadExtensionData(wall,ID):
	entity=DB.ExtensibleStorage.Entity(System.Guid(ID))
	schema=entity.Schema
	field=schema.GetField("LastTrySchema")
	retrievedEntity = wall.GetEntity( schema )
	retrievedData = retrievedEntity.Get[DB.XYZ](field, DB.DisplayUnitType.DUT_METERS)
	print(retrievedData)
	

#point=DB.XYZ(1,1,1)	
#c=CreatExtensionStorage(Picked_Selection,point)	
ReadExtensionData(Picked_Selection,"d64e3bab-7b93-415a-a20a-4d09ec106aaa")