# -*- coding: utf-8 -*-
__doc__="分析设计中内墙与外墙的量"
import sys
from pyrevit import revit,DB
from rpw import db

import clr
#clr.AddReference('libintl')
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *
#clr.AddReference('mscorlib')
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
from Revit.GeometryConversion import *
# Import ToProtoType, ToRevitType geometry conversion extension methods
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

#Wall = revit.pick_element().get_Geometry(DB.Options()).GetEnumerator()
Wall = revit.pick_element()
#Wall.MoveNext()
#C=Wall.Current
#print(C)
with db.Transaction('Move Beam To Floor'):
    Element=Wall.ToDSType(False)

print(Element)


#print (assembly.GetName().Name for assembly in clr.References)

