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


"""
EntitySchemaGuid=picked.GetEntitySchemaGuids()
schemaBuilder = DB.ExtensibleStorage.SchemaBuilder(System.Guid("d64e3bab-7b93-415a-a20a-4d09ec106aaa"))
schemaBuilder.SetReadAccessLevel(DB.ExtensibleStorage.AccessLevel.Public)
schemaBuilder.SetWriteAccessLevel(DB.ExtensibleStorage.AccessLevel.Public)
# schemaBuilder.SetVendorId("ADSK")
schemaBuilder.SetSchemaName("LastTrySchema")
fieldBuilder = schemaBuilder.AddSimpleField("LastTrySchema", DB.XYZ().GetType())
fieldBuilder.SetUnitType(DB.UnitType.UT_Length)
fieldBuilder.SetDocumentation("a wall.")
schema = schemaBuilder.Finish()

with revit.Transaction("Convert ACIS to FreeFrom"):
	ds = DB.DirectShape.CreateElement(doc, categoryId)
	ds.SetShape(new)
	ds.Name = "MyShape"
"""
for i in picked.get_Geometry(DB.Options ()):
	#for c in i.GetInstanceGeometry():
#		print(c)\
    print(i)

#new=List[DB.GeometryObject]()
#new.Add(c)
#categoryId =DB.ElementId(DB.BuiltInCategory.OST_GenericModel)



		
		






	